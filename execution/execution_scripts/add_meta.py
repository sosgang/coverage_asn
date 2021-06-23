import os
import json
import csv
import re
import unicodedata


def cleaning_doi(doi_raw):
    doi_clean = doi_raw.strip("doi: ").strip("https://dx.doi.org/").strip("#").replace(" ", "")
    doi_clean = doi_clean.lower()

    return doi_clean


def cleaning_title(title_raw):
    title_clean = u"".join(
        [c for c in unicodedata.normalize("NFKD", title_raw) if not unicodedata.combining(c)])  # remove accents
    title_clean = title_clean.lower()
    title_clean = re.sub(r" p$", "", title_clean)
    title_clean = re.sub(r"[^\w\d\s]", " ", title_clean)
    title_clean = re.sub(r"\s+", " ", title_clean)

    return title_clean


def clean_name(t, name_raw):
    if t == 1:
        name_clean = u"".join([c for c in unicodedata.normalize("NFKD", name_raw) if not unicodedata.combining(c)])
        name_clean = name_clean.lower()
        name_clean = re.sub(r"[^\w\d\s]", "", name_clean)
    else:
        name_clean = [clean_name(1, raw) for raw in name_raw]
    return name_clean


def matching_pubbs(list_pubbs, new):
    value = 0
    n = len(list_pubbs)
    idx = 0
    while idx < n:
        if "doi" in new.keys() and "doi" in list_pubbs[idx].keys():
            if new["doi"] == list_pubbs[idx]["doi"]:
                value = 1
                idx = n
        elif "title" in new.keys() and "title" in list_pubbs[idx].keys():
            if (new["title"].replace(" ", "") == list_pubbs[idx]["title"].replace(" ", "")
                    and new["year"] == list_pubbs[idx]["year"]):
                value = 1
                idx = n
        idx += 1

    return value


def extracting_cv(cand_dd, woinfo, cv_path):

    with open(cv_path, 'r') as json_file:
        data = json.load(json_file)
        cand_dd["pubbs"] = []
        idx_pubbs = 0
        empty_flag = True

        for pub in data["pubbs_ind"]:
            if "parsed" in pub.keys():
                if pub["parsed"] is not None:
                    empty_flag = False
                    d1 = dict()
                    d1['pub_idx'] = idx_pubbs
                    d1["year"] = int(pub["anno"])
                    if "type" in pub.keys():
                        d1["type"] = pub["type"].lower()
                    if "doi" in pub["parsed"].keys():
                        d1["doi"] = cleaning_doi(pub["parsed"]["doi"][0])
                    if "titolo" in pub["parsed"].keys():
                        d1["title"] = cleaning_title(pub["parsed"]["titolo"])
                    if "autori" in pub["parsed"].keys():
                        authors_raw = pub["parsed"]["autori"].split(", ")
                        d1["authors"] = clean_name(2, authors_raw)
                    cand_dd["pubbs"].append(d1)
                    idx_pubbs += 1
                    if "titolo" not in pub["parsed"].keys() and "doi" not in pub["parsed"].keys():
                        woinfo['lack_info_pub'].append(pub)
                else:
                    woinfo['unparsed_pub'].append(pub)
            else:
                woinfo['empty_pub'].append(pub)

        for pub in data["pubbs"]:
            if "parsed" in pub.keys():
                if pub["parsed"] is not None:
                    empty_flag = False
                    d2 = dict()
                    d2["year"] = int(pub["anno"])
                    if "type" in pub.keys():
                        d2["type"] = pub["type"].lower()
                    if "doi" in pub["parsed"].keys():
                        d2["doi"] = cleaning_doi(pub["parsed"]["doi"][0])
                    if "titolo" in pub["parsed"].keys():
                        d2["title"] = cleaning_title(pub["parsed"]["titolo"])
                    if "autori" in pub["parsed"].keys():
                        authors_raw = pub["parsed"]["autori"].split(", ")
                        d2["authors"] = clean_name(2, authors_raw)

                    value = matching_pubbs(cand_dd["pubbs"], d2)
                    if value == 0:
                        d2['pub_idx'] = idx_pubbs
                        cand_dd["pubbs"].append(d2)
                        idx_pubbs += 1

                    if "titolo" not in pub["parsed"].keys() and "doi" not in pub["parsed"].keys():
                        woinfo['lack_info_pub'].append(pub)
                else:
                    woinfo['unparsed_pub'].append(pub)
            else:
                woinfo['empty_pub'].append(pub)

        if empty_flag:
            cand_dd['pubbs_ind'] = data['pubbs_ind']
            cand_dd['pubbs'] = data['pubbs']
            woinfo['empty_cvs'].append(cand_dd)


def finding_metadata(meta_d, woinfo_d, tsv_path, cvs_folder_path):
    woinfo_d['missing_cvs'] = []
    woinfo_d["empty_cvs"] = []
    woinfo_d["empty_pub"] = []
    woinfo_d["unparsed_pub"] = []
    woinfo_d["lack_info_pub"] = []

    with open(tsv_path, 'r', encoding='utf-8') as tsv_file:
        ind_anvur_tsv = csv.reader(tsv_file, delimiter="\t")
        for row in ind_anvur_tsv:
            if row[1] != "annoAsn":
                if row[1] not in meta_d.keys():
                    meta_d[row[1]] = dict()
                if row[4] not in meta_d[row[1]].keys():
                    meta_d[row[1]][row[4]] = dict()
                if row[5] == "1":
                    role = "FP"
                elif row[5] == "2":
                    role = "AP"
                if role not in meta_d[row[1]][row[4]].keys():
                    meta_d[row[1]][row[4]][role] = dict()
                if row[2] not in meta_d[row[1]][row[4]][role].keys():
                    meta_d[row[1]][row[4]][role][row[2]] = dict()
                if row[0] not in meta_d[row[1]][row[4]][role][row[2]].keys():
                    meta_d[row[1]][row[4]][role][row[2]][row[0]] = dict()

                cand_d = meta_d[row[1]][row[4]][role][row[2]][row[0]]
                cand_d["fullname"] = [clean_name(1, row[7]), clean_name(1, row[8])]
                cand_d['cv_id'] = [row[1], row[4], role, row[2], row[0]]

                cand_cv_path = os.path.join(cvs_folder_path, row[1], row[4], role, row[2], row[0]+'.json')
                if os.path.exists(cand_cv_path):
                    extracting_cv(cand_d, woinfo_d, cand_cv_path)
                else:
                    woinfo_d['missing_cvs'].append(cand_d)
