# coverage_asn

Repository containing code and results for our **"   "** paper.

1. [Introduction](#1-introduction)
2. [Results](#2-Results)
3. [Preparing the data](#3-preparing-the-data)
4. [Executing searches to find coverage](#4-executing-searches-to-find-coverage)

## 1. Introduction

abstract

## 2. Results

Due to Github's limit on files' size, we are unable to upload the complete results of our study. They are available on Zenodo (link) in the folder **"results"**.

- [**cov_asn_xcand.csv**](https://github.com/sosgang/coverage_asn/blob/main/execution/cov_asn_xcand.csv) contains the coverage information calculated for each candidate. Each row corresponds to one candidate. The columns are the following:
  - "term" : term the candidate applied in.
  - "role" : role the candidate applied for.
  - "field" : field the candidate applied for.
  - "id" : unique ID of the application.
  - "total_CV" : total number of unique publications from the candidate's CV.
  - "MAG" : raw number of publications from the candidate's CV found in Microsoft Academic Graph.
  - "OA" : raw number of publications from the candidate's CV found in OpenAIRE.
  - "CR" : raw number of publications from the candidate's CV found in CrossRef.
  - "comb" : raw number of publications from the candidate's CV found when the open sources of use are combined.
  - "MAG% : percentage of publications from the candidate's CV found in Microsoft Academic Graph.
  - "OA%" : percentage of publications from the candidate's CV found in OpenAIRE.
  - "CR%" : percentage of publications from the candidate's CV found in Crossref.
  - "comb%" : percentage of publications from the candidate's CV found when MAG, OpenAIRE and Crossref are combined.

- [**cov_asn_xdataset.csv**](https://github.com/sosgang/coverage_asn/blob/main/execution/cov_asn_xdataset.csv) contains the coverage information broken down for each dataset. Each row corresponds to percentage of publications found in that dataset for a single candidate. The columns are the following:
  - "dataset" : dataset of interest.
  - "term" : term the candidate applied in.
  - "role" : role the candidate applied for.
  - "SA" : scientific area the candidate applied for
  - "field" : field the candidate applied for.
  - "role&field" : combination of role and field the candidate applied for.
  - "coverage%" : percentage of publications from the candidate's CV found when MAG, OpenAIRE and Crossref are combined.

- [**cov_asn_xyear.csv**](https://github.com/sosgang/coverage_asn/blob/main/execution/cov_asn_xyear.csv) contains the coverage information calculated for each year. Each row corresponds to one year. The columns are the following:
  - "year" : year of publication.
  - "total" : total number of unique publications published in that year from all the candidates' CVs.
  - "MAG" : raw number of publications published in that year found in Microsoft Academic Graph.
  - "OA" : raw number of publications published in that year found in OpenAIRE.
  - "CR" : raw number of publications published in that year found in CrossRef.
  - "comb" : raw number of publications published in that year found when the open sources of use are combined.
  - "MAG% : percentage of the number of publications published in that year found in Microsoft Academic Graph.
  - "OA%" : percentage of publications published in that year found in OpenAIRE.
  - "CR%" : percentage of publications published in that year found in Crossref.
  - "comb%" : percentage of publications published in that year found when MAG, OpenAIRE and Crossref are combined.

## 3. Preparing the data

To investigate coverage in our open access datasets of interest, we create a MongoDB database using data from the Microsoft Academic Graph Dump, OpenAIRE Research Graph Dump and Crossref Public Data File. We then query this database with publications' metadata extracted from the candidates' CVs so as to assess whether said publications are present in the datasets of interest.

### 3.1 Processing MAG's, OA's and CR's Dumps

Due to Github's limit on files' size, we are unable to upload the processed versions dumps here. However, we provide download links to the original dumps and instructions to replicate our processing. The processed and ready-to-use dumps is available on Zenodo (link) in the folder **"final"**.

1. Download the folder **"preparation"** from this repo
2. Download all the dumps in a folder named **"originals"** inside **"preparation"** from the following links:
  - [Microsoft Academic Graph Dump](https://archive.org/details/mag-2020-01-23)
  - [OpenAIRE Research Graph Dump](https://zenodo.org/record/4707307)
  - [Crossref Public Data File](https://academictorrents.com/details/e4287cb7619999709f6e9db5c359dda17e93d515)
2. Decompress Microsoft Academic Graph's dump in a folder named **"mag"** inside **"preparation"**
3. Decompress OpenAIRE's dump in a folder named **"openaire"** inside **"preparation"**
4. Decompress Crossref's dump in a folder named **"crossref"** inside **"preparation"**
5. Execute [**coverage_asn_preparation.py**](https://github.com/sosgang/coverage_asn/blob/main/preparation/coverage_asn_preparation.py): this script cleans and processes all the data in the dumps and stores them as separate jsons in a folder named "final" inside "preparation". It also imports the dumps as single collections into a MongoDB database and creates the necessary indexes in the collections. If these two other steps are not of interest to you, comment out the *importing_dumps_to_db(output_dir)* and *create_indexes_in_db()* functions at the end of the python file.


Estimated time: _processing one dump takes approximately 4h on our machine_

### 3.2 Setting the database

1. Follow the steps in section 3.1 above OR Download the folder named **"preparation"** from Zenodo (link)
2. Execute [**coverage_asn_preparation.py**](https://github.com/sosgang/coverage_asn/blob/main/preparation/coverage_asn_preparation.py): if there is a folder named "final" in "preparation" the script doesn't processes the dumps (it doesn't execute the function *processing*). It imports the dumps as single collections into a MongoDB database and creates the necessary indexes in the collections. If either of these two steps are not of interest to you, comment out either the *importing_dumps_to_db* or the *create_indexes_in_db* function at the end of the python file.


Estimated times:
  - _importing one dump to the database took approximately 1.5h on our machine_
  - _creating a textual index in one collection took from 3 to 4 hours on our machine, ascending/descending indexes take far less_

## 4. Executing searches to find coverage

Once our MongoDB database is set, we can query it to search for the candidates' publications and assess whether they are present in the different datasets. To set your database follow the steps in section 3 above. Due to Github's limit on files' size, we are unable to upload the folder with all the candidates' CVs from which we estract the publications' metadata to query the database with. However, they are available on Zenodo (link) in the folder **"cand_cvs"**.

1. Download the folder **"execution"** from this repo
2. Execute [**coverage_asn_execution.py**](https://github.com/sosgang/coverage_asn/blob/main/execution/coverage_asn_execution.py): this script extracts publications' metadata from each candidate's CV, searches for the publication in the Microsoft Academic Graph, OpenAIRE and Crossref collections of the database and calculates coverage of the candidate's publications by these datasets. Specifically it stores results in several files in the folder named **"results"** in the folder **"execution"**:
  - In **meta_dict.json**, it stores the publications' metadata extracted from the CVs.
  - In **wo_ info.json**, it stores information about missing CVs, CVs with no publications, publications incorrectly parsed from PDF, empty publications, and publications missing both title and doi.
  - For each candidate, it stores the publications' data found in the database and the coverage data in a new separate json file in **"results"**. There, resulting candidates' json files are organized by the term, role, and field they applied for in the 2016-18 NSQ session.
  - Finally, it stores the essential results into the two csv files in the folder **"execution"**, [cov_asn_xcand.csv](https://github.com/sosgang/coverage_asn/blob/main/execution/cov_asn_xcand.csv), [cov_asn_xdataset.csv](https://github.com/sosgang/coverage_asn/blob/main/execution/cov_asn_xdataset.csv) and [cov_asn_xyear.csv](https://github.com/sosgang/coverage_asn/blob/main/execution/cov_asn_xyear.csv).
