# LB2_project_Group_3
this repository contains files of the project for the Laboratory of Bioinformatics 2 course


This is the Query of Uniprot search of positive set:
(existence:1) AND (length:[40 TO *]) AND (reviewed:true) AND (taxonomy_id:2759) AND (fragment:false) AND (ft_signal_exp:*)


This is the API search endpoint of the positive set
https://rest.uniprot.org/uniprotkb/search?compressed=true&format=fasta&query=%28%28existence%3A1%29+AND+%28length%3A%5B40+TO+*%5D%29+AND+%28reviewed%3Atrue%29+AND+%28taxonomy_id%3A2759%29+AND+%28fragment%3Afalse%29+AND+%28ft_signal_exp%3A*%29%29&size=500