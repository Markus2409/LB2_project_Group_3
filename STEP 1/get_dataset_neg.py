import requests
from requests.adapters import HTTPAdapter, Retry
import json
import re

retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))

def get_next_link(headers):

    ''' function to get the link for the next batch of entries, the function terminates when the link is not found'''
 
    if "Link" in headers:
        # The regular expression is used to extract the next link for pagination
        re_next_link = re.compile(r'<(.+)>; rel="next"')
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)

def get_batch(batch_url):

    '''generator function that yields each batch generated with the current API call link '''

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

batch_size = 500
url_neg = "https://rest.uniprot.org/uniprotkb/search?format=json&query=%28%28fragment%3Afalse%29+AND+%28length%3A%5B40+TO+*%5D%29+AND+%28taxonomy_id%3A2759%29+NOT+%28ft_signal%3A*%29+AND+%28%28cc_scl_term_exp%3ASL-0091%29+OR+%28cc_scl_term_exp%3ASL-0191%29+OR+%28cc_scl_term_exp%3ASL-0173%29+OR+%28cc_scl_term_exp%3ASL-0209%29+OR+%28cc_scl_term_exp%3ASL-0204%29+OR+%28cc_scl_term_exp%3ASL-0039%29%29+AND+%28reviewed%3Atrue%29+AND+%28existence%3A1%29%29&size=500"
output_file = "negative_dataset.tsv"


def extract_fields(entry):

    '''function to extract the fields of interest from the JSON of each entry '''
    
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


def get_dataset(search_url, extract_function, output_file_name):

    '''function to get the entire dataset. It uses all the previous functions '''

    dataset_json = []
    n_total = 0
    for batch, total in get_batch(search_url):
        batch_json = json.loads(batch.text)
        print("Status code:", batch.status_code)
        print("Content-Type:", batch.headers.get("Content-Type"))
        print("Text preview:", batch.text[:200]) 
        for entry in batch_json["results"]:
            n_total += 1
            dataset_json.append(extract_function(entry))
    print(n_total)
    with open(output_file_name, "w") as ofs:
        for entry in dataset_json:
            print(*entry, sep="\t", file=ofs)
        ofs.close

if __name__ == "__main__":
    get_dataset(url_neg, extract_fields, output_file)
