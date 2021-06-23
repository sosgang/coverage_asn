# coverage_asn

Repository containing code and results for our **"   "** paper.

1. [Introduction](#1-introduction)
2. [Results](#2-Results)

## 1. Introduction

abstract

## 2. Results

### 2.1 Coverage data

- [**coverage.csv**](https://github.com/sosgang/bond/blob/main/coverage/coverage.csv) contains the coverage information calculated for each candidate. Each row corresponds to one candidate. The columns are the following:
  - "term" : term the candidate applied in.
  - "role" : role the candidate applied for.
  - "field" : field the candidate applied for.
  - "id" : unique ID of the application.
  - "MAG" : raw number of publications authored by the candidate found in Microsoft Academic Graph.
  - "OA" : raw number of publications authored by the candidate found in OpenAIRE.
  - "CR" : raw number of publications authored by the candidate found in CrossRef.
  - "comb" : raw number of publications found when the open sources of use are combined.
  - "MAG% : percentage of the number of publications authored by the candidate found in Microsoft Academic Graph over the total number of unique publications in the CV.
  - "OA%" : percentage of the number of publications authored by the candidate found in OpenAIRE over the total number of unique publications in the CV.
  - "CR%" : percentage of the number of publications authored by the candidate found in Crossref over the total number of unique publications in the CV.
  - "comb%" : percentage of the number of publications authored by the candidate found over the total number of unique publications in the CV when the open sources of use are combined.
  - "total_CV" : total number of unique publications in the candidate's cv
