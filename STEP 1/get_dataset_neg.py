import requests
from requests.adapters import HTTPAdapter, Retry
import json
import re

retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))

def get_next_link(headers):
    if "Link" in headers:
        # The regular expression is used to extract the next link for pagination
        re_next_link = re.compile(r'<(.+)>; rel="next"')
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)

# This function actually retrieve the next data batch in the search.
# The function act as an iterator, yielding the next result batch at every call
# The function terminates after the last batch has been returned. In this case,
# the next link will be None
def get_batch(batch_url):
    while batch_url:
        # Run the API call
        response = session.get(batch_url)
        # Will raise an error if an error status code is obtained
        response.raise_for_status()
        # Get the total number of entries in the search
        total = response.headers["x-total-results"]
        # Yield the response and the total number of entries
        yield response, total
        # Get the link to the API call for the next data batch
        batch_url = get_next_link(response.headers)


# We define a basic URL for the search.
# We look for all non-fragment reviewed human protein having a coiled-coil region in the first 100 residues.
# The URL has been generated from the UniProtKB website, using the
# Advanced search function.
batch_size = 500
url_neg = "https://rest.uniprot.org/uniprotkb/search?format=json&query=%28%28fragment%3Afalse%29+AND+%28length%3A%5B40+TO+*%5D%29+AND+%28taxonomy_id%3A2759%29+NOT+%28ft_signal%3A*%29+AND+%28%28cc_scl_term_exp%3ASL-0091%29+OR+%28cc_scl_term_exp%3ASL-0191%29+OR+%28cc_scl_term_exp%3ASL-0173%29+OR+%28cc_scl_term_exp%3ASL-0209%29+OR+%28cc_scl_term_exp%3ASL-0204%29+OR+%28cc_scl_term_exp%3ASL-0039%29%29+AND+%28reviewed%3Atrue%29+AND+%28existence%3A1%29%29&size=500"
# To only include proteins with a coiled-coil in the first 100 residues, we define a filter function
# It returns True if the entry passess the filter, False otherwise

def filter_entry(entry):
    # We iterate over the features of the entry
    for feature in entry["features"]:
        # We only consider features of type Coiled coil
        if feature["type"] == "Coiled coil":
            # Check if the coiled-coil starts before position 100
            if feature["location"]["start"]["value"] < 100:
                return True
    return False

# We set the name of the output file, we want TSV output
output_file = "negative_dataset.tsv"

# We define a function to better control the TSV format in output.
# In particular, we run the API call requiring JSON format and build our own TSV file
# The this aim, the following function extract and process specific fields from the JSON file

def extract_fields(entry):
    # We extract the accession, organism name, Eukariotic kingdom, protein lenght, transmembrane helix starting in 90 residues (True or False)
    pa = entry["primaryAccession"]
    name = entry["organism"]["scientificName"]
    lin = entry["organism"]["lineage"][1]
    lenn = entry["sequence"]["length"]
    hel = "False"
    for feature in entry["features"]:
        if feature["type"] == "Helix":
            if feature["location"]["start"]["value"] < 90:
                hel = "True"
                break
    return (pa , name , lin , lenn , hel)

    
    # We iterate over the features of the entry
    for f in entry["features"]:
        # We only consider the first coiled-coil segment
        if f["type"] == "Coiled coil":
            s = f["location"]["start"]["value"]
            e = f["location"]["end"]["value"]
            break
    return (entry["primaryAccession"], entry["sequence"]["length"], s, e)


def get_dataset(search_url, extract_function, output_file_name):
    filtered_json = []
    n_total, n_filtered = 0, 0
    # Run the API call in batches
    for batch, total in get_batch(search_url):
        # parse the JSON body of the response
        batch_json = json.loads(batch.text)
        print("Status code:", batch.status_code)
        print("Content-Type:", batch.headers.get("Content-Type"))
        print("Text preview:", batch.text[:200])  # prime 200 caratteri
        for entry in batch_json["results"]:
            n_total += 1
            filtered_json.append(extract_function(entry))
    print(n_total)
    with open(output_file_name, "w") as ofs:
        for entry in filtered_json:
            print(*entry, sep="\t", file=ofs)
        ofs.close


get_dataset(url_neg, extract_fields, output_file)
