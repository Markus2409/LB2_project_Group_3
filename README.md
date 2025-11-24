
# **A Cross-Model Comparison of Secretiory Signal Peptide Prediction Techiques: Von Hijne, SVM, NN**

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python&logoColor=white)
![PyTorch](https://img.shields.io/badge/PyTorch-1.14-orange?logo=pytorch&logoColor=white)
![SVM & NN](https://img.shields.io/badge/Methods-SVM%20%26%20NN-green)
![Bioinformatics](https://img.shields.io/badge/Field-Bioinformatics-purple)
![License: MIT](https://img.shields.io/badge/License-MIT-lightgrey)

## **Laboratory of Bioinformatics 2, A.Y. 2025/2026**

Cagnini Luca,  Centenaro Marco,  Cuscunà Marco,  Mariano Marina,  Timelli Giacomo 

Bioinformatics, FABIT, Alma Mater Studiorum – University of Bologna, Italy

---

## **Abstract**
This repository contains files and codes of the project for the **Laboratory of Bioinformatics 2 course**. The aim of the project was to analyze and compare three different **computational approaches** for the prediction of **Signal peptides (SPs)**. 
Signal peptides (SPs) are short, essential sequences that guide proteins to their
correct cellular locations, significantly influencing protein functionality and various cellular processes.
While numerous computational methods exist for SP prediction, machine learning techniques,
particularly **Support Vector Machines (SVM)** and **Neural Networks**, have shown substantial
improvements over traditional methods like the **Von Heijne algorithm**. 
**Results:** The aim of the study is to confirm this hypothesis developing a correct workflow that higlights significant improvement on protein predictions of the firs two methods previously mentioned over the latter.  

---
# Table of Contents

1. [Data Collection](#data-collection)  
2. [Data_Preparation](#data-preparation)  
3. [Data_analysis](#data-analysis)  
4. [Von Heijne](#von-heijne)  
5. [SVM: Feature Selection](#svm-feature-selection)  
6. [Deep_Learning: LSTM](#deep-learning-lstm)
7. [Model performances](#model-performances)
8.  [Discussion](#discussion)
---

# Data Collection

Repository: [Data_collection](./Data_Collection)

The first step of the analysis was to retrieve relevant datasets of protein sequences from UniProtKB. Two proteins datasets were created, a positive one containing the signal peptide, and a negative one with all the others. This approach included two step:
- Web interface approach: advance query search using web interface. 
- API approach: APi call to the UniProtKB/swiss-Prot database.


 ## Results 

Results were saved in two .tsv files: [positive_dataset.tsv], (Data_Collection/positive_dataset.tsv) [negative_dataset.tsv](/Data_collection/negative_dataset.tsv). 

 | Positive Set | Negative Set | Negative with HD | 
|--------------|--------------|------------------|
|  2932        |    20615     |      1384        |

---

# Data Preparation

Repository: [Data_Preparation](./Data_Preparation)

This step included the preprocessing pipeline datasets for cross-validation and benchmarking, including:
- training and benchmark set creation: splitting positive and negative datasets into two subsets
- redundancy reduction: performend using the MMseqs2 clustering tool

## Results 

Results of our analysis were saved on the file [train_bench.tsv](./Data_Preparation/train_bench.tsv). 

|       Dataset          |        Negatives        |     Positives      |  
|-------------------------|-------------------------|-------------------|
|  Training Sets (total)  |          7147           |       874         |  
| Benchmark Set           |          1787           |       219         |
| Total                   |          8934           |       1093        |


---

# Data Analysis
Repository: [Data-analysis](./Data_Analysis)

An exploratory statistical analysis of the datasets was essential to asses adequacy of the datasets for our porpouse, aimed to confirm dataset quality. 
- Detect dataset **biases** (length, amino acid composition, taxonomy).
- Assess whether sequence properties are **informative features** for classification tasks.
- Evaluate differences between **training** and **benchmarking** datasets.
- gain an insight about data quality across datasets (benchmark/training).

## Results
Resulting plot were saved on three folders:
- [SequenceLogo](/Data_Analysis/SequenceLogo) Contains sequence logo visualizations representing conserved regions and amino acid preferences across datasets.
- [Sequence_lengths_comparison](/Data_Analysis/Sequence_lengths_comparison) Includes analyses and plots comparing sequence length distributions between datasets.
- [Taxonomy_classification](/Data_Analysis/Taxonomy_classification) Provides taxonomic classification summaries, exploring the distribution of sequences across taxonomic groups. 

---

# Von Heijne

Repository: [von_Heijne](./vonHeijne)

Von Heijne’s algorithm was developed by Gunnar von Heijne in the 1980s–1990s, often used in combination with experimental data to analyze protein targeting. Implementation involved the creation of a PSWM (position specific weight metric combined with a 5-fold cross validation method, using appropirate measures for testing our analysis. 

## Results 
After cross-validation method, a mean value of each metric was calculated and it is shown below. 

 | Metric      | Mean ± Std  |
|------------|-------------|
| MCC        | 0.663 ± 0.016 |
| Precision  | 0.934 ± 0.003 |
| Accuracy   | 0.691 ± 0.014 |
| Sensitivity| 0.711 ± 0.029 |

---

# SVM: Feature Selection 

Repository: [Feature_Selection](./Feature_Selection)

The SVM (support Vector Machine) algorithm was trained using a Feature extraction and selection procedure, taking into account several characteristics of the proteins dataset. It was implemented using Random Forest and SVM training optimized by 5 fold cross validation. 
Results show strong and consistent predictive performance, with average MCC scores between 0.84 and 0.88 across all folds.

## Performance Summary

| Fold | Best k | Validation MCC | Test MCC |
|------|--------:|----------------:|----------:|
| 1 | 27 | 0.868 | 0.825 |
| 2 | 28 | 0.877 | 0.862 |
| 3 | 13 | 0.839 | 0.854 |
| 4 | 11 | 0.857 | 0.798 |
| 5 | 35 | 0.845 | 0.883 |

**Average Test MCC:** ≈ **0.84–0.88**

---

#  Deep Learning: LSTM

Repository: [Deep_Learning](./Deep_Learning/)

The model is a hybrid **CNN-LSTM** that extracts local features with convolutional layers and captures long-range dependencies with LSTM layers.  
A dynamic fully connected **MLP head** performs binary classification on the processed sequence features.  
Training includes early stopping and gradient clipping to ensure robust learning.  

## Results 
On the benchmark fold, the model achieves an **MCC of ~0.902**, demonstrating strong predictive performance.

# Model Performances 

Repository; [Model_Performances](./Model_performances)

A comparative evaluation of multiple classification models was performed. The goal was to measure and compare model performance using robust metrics such as Matthews Correlation Coefficient (MCC) and standard classification scores as well as getting insights about the biological reasons under our results. 

## Performances Summary 

 | Metod     |   MCC  |
|------------|--------|
| VonHeijne  | 0.688  |
| SVM        | 0.808  |
| DL         | 0.902  |

---

# 8. Discussion

## Summary Performance of three models: Von Heijne, SVM, and LSTM

### 1. Von Heijne
**The Von Heijne model**, based solely on amino acid frequencies, served as a baseline and performed poorly. It showed high false positive rates, particularly for transmembrane (TM) proteins, highlighting that signal peptides and TM domains share similar amino acid composition, which easily misled the model compared to SVM. 

### 2. SVM
**The SVM classifier** achieved low overall FPR, although TM helices remained a common source of misclassification. False negatives were slightly more frequent in short signal peptides (<15 residues), while longer peptides were generally classified correctly. Amino acid composition played a key role in both false positives and false negatives, and plant transit peptides did not significantly confound performance (FPR ~2.2%), though Arabidopsis sequences showed a slightly higher FPR.

### 3. LSTM
**LSTM** outperformed SVM in overall MCC, as well as in FP and FN counts. TM proteins were still misclassified (41.2% of FPs), and longer signal peptides (>35 residues) tended to be false negatives. Taxon-specific differences were observed: FPR decreased in plant proteins but increased in fungi and other groups. Sequence features such as leucine frequency in the first positions of the signal peptide appeared important for correct classification.

---
# 9. Conclusions

The objective of this project was to develop and evaluate computational models for signal peptide (SP) prediction. Three approaches were compared: the von Heijne algorithm (VH), Support Vector Machines (SVM), and a Deep Learning.

Overall, both **SVM** and **NN** are robust classifiers for signal peptide prediction, with the Neural Network showing superior performance. Misclassifications are primarily driven by TM domains, signal peptide length, and amino acid composition. Transit peptides in plants, have minimal impact on classifier performance, suggesting these models can reliably distinguish signal peptides from similar N-terminal sequences. This work emphasizes the importance of careful feature selection and model choice in bioinformatic prediction tasks.

# Contacts
- Giacomo Timelli - giacomo.timelli@studio.unibo.it
- Luca Cagnini - luca.cagnini@studio.unibo.it
- Marco Centenaro - marco.centenaro@studio.unibo.it
- Marco Cuscunà - marco.cuscuna@studio.unibo.it
- Marina Mariano - marina.mariano@studio.unibo.it

