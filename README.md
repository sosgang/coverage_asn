# coverage_asn

Repository containing code and results for our **"   "** paper.

1. [Introduction](#1-introduction)
2. [Results](#2-Results)
3. [Preparing the data](#3-preparing-the-data)

## 1. Introduction

abstract

## 2. Results

- [**coverage_asn.csv**](https://github.com/sosgang/coverage_asn/blob/main/execution/coverage_asn.csv) contains the coverage information calculated for each candidate. Each row corresponds to one candidate. The columns are the following:
  - "term" : term the candidate applied in.
  - "role" : role the candidate applied for.
  - "field" : field the candidate applied for.
  - "id" : unique ID of the application.
  - "total_CV" : total number of unique publications from the candidate's CV.
  - "MAG" : raw number of publications from the candidate's CV found in Microsoft Academic Graph.
  - "OA" : raw number of publications from the candidate's CV found in OpenAIRE.
  - "CR" : raw number of publications from the candidate's CV found in CrossRef.
  - "comb" : raw number of publications from the candidate's CV found when the open sources of use are combined.
  - "MAG% : percentage of the number of publications from the candidate's CV found in Microsoft Academic Graph over the total number of unique publications in the CV.
  - "OA%" : percentage of the number of publications from the candidate's CV found in OpenAIRE over the total number of unique publications in the CV.
  - "CR%" : percentage of the number of publications from the candidate's CV found in Crossref over the total number of unique publications in the CV.
  - "comb%" : percentage of the number of publications from the candidate's CV found over the total number of unique publications in the CV when the open sources of use are combined.


- [**cov_years_asn.csv**](https://github.com/sosgang/coverage_asn/blob/main/execution/cov_years_asn.csv) contains the coverage information calculated for each year. Each row corresponds to one year. The columns are the following:
  - "year" : year of publication.
  - "total" : total number of unique publications published in that year from all the candidates' CVs.
  - "MAG" : raw number of publications published in that year found in Microsoft Academic Graph.
  - "OA" : raw number of publications published in that year found in OpenAIRE.
  - "CR" : raw number of publications published in that year found in CrossRef.
  - "comb" : raw number of publications published in that year found when the open sources of use are combined.
  - "MAG% : percentage of the number of publications published in that year found in Microsoft Academic Graph over the total number of publications from that year.
  - "OA%" : percentage of the number of publications published in that year found in OpenAIRE over the total number of publications from that year.
  - "CR%" : percentage of the number of publications published in that year found in Crossref over the total number of publications from that year.
  - "comb%" : percentage of the number of publications published in that year found over the total number of publications from that year.

## 3. Preparing the data

Due to Github's limit on files' size, we are unable to upload the original and processed dumps here. However, we provide download links to the original dumps and instructions to replicate our study. Ready-to-use data and code is available on Zenodo (link).

### 3.1 Processing MAG's, OA's and CR's Dumps

1. Download the folder **"preparation"** from this repo
2. Download all the dumps in a folder named **"originals" inside "preparation"** from the following links:
  - [Microsoft Academic Graph Dump](https://archive.org/details/mag-2020-01-23)
  - [OpenAIRE Research Graph Dump](https://zenodo.org/record/4707307)
  - [Crossref Public Data File](https://academictorrents.com/details/e4287cb7619999709f6e9db5c359dda17e93d515)
2. Decompress Microsoft Academic Graph's dump in a folder named **"mag" inside "preparation"**
3. Decompress OpenAIRE's dump in a folder named **"openaire" inside "preparation"**
4. Decompress Crossref's dump in a folder named **"crossref" inside "preparation"**
5. Execute [**coverage_asn_preparation.py**](https://github.com/sosgang/coverage_asn/blob/main/preparation/coverage_asn_preparation.py): this script cleans and processes all the data in the dumps and stores them as separate jsons in a folder named **"final"** inside "preparation". It also imports the dumps as collections to a MongoDB database and creates the necessary indexes in the collections. If these two other steps are not of interest to you, comment out the **importing_dumps_to_db(output_dir)** and **create_indexes_in_db()** functions at the end of the python file.

### 3.2 Setting the database

1.
  a. Follow the steps in section 3.1 above
  b. Download the folder named **"preparation"** from this repo and download the folder named **"final" inside "preparation"** from Zenodo (link)
  c. Download the folder named **"preparation"** from Zenodo (link)
2. Execute [**coverage_asn_preparation.py**](https://github.com/sosgang/coverage_asn/blob/main/preparation/coverage_asn_preparation.py): if there is a folder named "final" in "preparation" the script doesn't processes the dumps. It imports the dumps as collections to a MongoDB database and creates the necessary indexes in the collections. If either of these two steps are not of interest to you, comment out either the **importing_dumps_to_db(output_dir)** or the **create_indexes_in_db()** function at the end of the python file.

## 3. Preparing the data
