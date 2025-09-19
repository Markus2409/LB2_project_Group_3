# ***DATA COLLECTION***
The first step for the project is *data collection* : for any machine learning model it is always necessary to acquire high-quality data,
to ensure the correct traning of it. We retrived relevant protein sequences from Uniprot database, filtering and creating 
two different datasets:a positive and a negative one. 
Our approach was divided into two consecutive step: a first data retrival of proteins using the Web interface approach, and a second one, using the API of UniProt database from the first advanced search. 
## 1. Web interface approach
We started using the Advance search interface in Uniprot (Release 2025_03) (https://www.uniprot.org/) to filter out and retrive the API for two sets of proteins:
### Positive Set
**QUERY:** 
```
(existence:1) AND (length:[40 TO ]) AND (reviewed:true) AND (taxonomy_id:2759) AND (fragment:false) AND (ft_signal_exp:)

```
- *existence:1* → protein existence at protein level (experimental evidence)  
- *length:[40 TO ]* → sequence length ≥ 40 aa  
- *reviewed:true* → only proteins reviewed in UniProtKB/Swiss-Prot  
- *taxonomy_id:2759* → proteins from the taxon Eukaryota  
- *fragment:false* → exclude fragments (only complete proteins)  
- *ft_signal_exp:* → proteins with feature signal peptide (experimental evidence)  

**Result:** 

Curated eukaryotic proteins, ≥40 aa, experimentally confirmed, non-fragment, with an experimentally validated signal peptide. For uniprot the API was retrived. 
The API URL using the search endpoint for positive set was retrived. This endpoint is lighter and returns chunks of 500 at a time and requires pagination: 

https://rest.uniprot.org/uniprotkb/search?format=json&query=%28%28existence%3A1%29+AND+%28length%3A%5B40+TO+*%5D%29+AND+%28reviewed%3Atrue%29+AND+%28taxonomy_id%3A2759%29+AND+%28fragment%3Afalse%29+AND+%28ft_signal_exp%3A*%29%29&size=500

### Negative set
*QUERY:*
 ```
 (existence:1) AND (length:[40 TO ]) AND (reviewed:true) AND (taxonomy_id:2759) AND (fragment:false) NOT (ft_signal:) AND 
 ((cc_scl_term_exp:SL-0091) OR (cc_scl_term_exp:SL-0191) OR (cc_scl_term_exp:SL-0173) OR (cc_scl_term_exp:SL-0209) OR (cc_scl_term_exp:SL-0204) OR (cc_scl_term_exp:SL-0039))
```
- *existence:1* → protein existence at protein level (experimental evidence)  
- *length:[40 TO ]* → sequence length ≥ 40 aa  
- *reviewed:true* → Swiss-Prot (manually curated)  
- *taxonomy_id:2759* → Eukaryota  
- *fragment:false* → exclude fragments  
- *NOT (ft_signal:)* → no signal peptide  
- *cc_scl_term_exp:*  
  - SL-0091 → Cytoplasm  
  - SL-0191 → Nucleus  
  - SL-0173 → Mitochondrion  
  - SL-0209 → Plastid  
  - SL-0204 → Peroxisome  
  - SL-0039 → Endoplasmic reticulum
  
**Result:**  

Curated eukaryotic proteins, ≥40 aa, experimentally confirmed, non-fragment, without signal peptide, localized experimentally to one of the listed compartments.
the API URL using the search endpoint for negative set was downloaded. This endpoint is lighter and returns chunks of 500 at a time and requires pagination.

https://rest.uniprot.org/uniprotkb/search?format=json&query=%28%28fragment%3Afalse%29+AND+%28length%3A%5B40+TO+*%5D%29+AND+%28taxonomy_id%3A2759%29+NOT+%28ft_signal%3A*%29+AND+%28%28cc_scl_term_exp%3ASL-0091%29+OR+%28cc_scl_term_exp%3ASL-0191%29+OR+%28cc_scl_term_exp%3ASL-0173%29+OR+%28cc_scl_term_exp%3ASL-0209%29+OR+%28cc_scl_term_exp%3ASL-0204%29+OR+%28cc_scl_term_exp%3ASL-0039%29%29+AND+%28reviewed%3Atrue%29+AND+%28existence%3A1%29%29&size=500

## 2. API approach

Two python scripts  (*get_dataset_neg.ipynb* *get_dataset_pos.ipynb*) were created to perform the API search of Uniprot, to create two output file format (.tsv .fasta) of our sets and to add a more precise filtering step that included: 
- Filtering out proteins with a SP shorter than 14 residues and without a cleavage site for the positive set
- Checking for proteins with a transmembrane helix starting in the first 90 residues
  
## 3. Data output

After the API call, our data were saved in a *.tsv* format to include informations specific to each protein 
(for the positive set: the protein UniProt accession, the organism name, the Eukaryotic kingdom, the protein length, the position of the signal peptide cleavage site)
(for the negative set: the protein UniProt accession, the organism name, the Eukaryotic kingdom, the protein length, Whether the protein has a transmembrane helix starting in the first 90 residues). 
Sequences were saved in a *.fasta* file. 
The number of proteins for each set is showed in the table below. 

| Positive Set | Negative Set | Helix Domain |
|--------------|--------------|--------------|
|  2932        |    20615     |      4414    |
|









