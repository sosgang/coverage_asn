import os
import json
import unicodedata
import re


def clean_title(title_raw):
    title_clean = u"".join([c for c in unicodedata.normalize("NFKD", title_raw) if not unicodedata.combining(c)])
    title_clean = title_clean.lower()
    title_clean = re.sub(r"[^\w\d\s]", " ", title_clean)
    title_clean = re.sub(r"\s+", " ", title_clean)

    return title_clean


def clean_name(name_raw):
    name_clean = u"".join([c for c in unicodedata.normalize("NFKD", name_raw) if not unicodedata.combining(c)])
    name_clean = name_clean.lower()
    name_clean = re.sub(r"[^\w\d\s]", "", name_clean)

    return name_clean


def cleaning_mag_file(in_path):
    output_path = os.path.join(in_path[:-4].lower())

    if "Papers" in in_path:
        with open(in_path, "r", encoding="utf-8") as original:
            for line in original:
                split_line = line.strip("\n").split("\t")
                info = [split_line[0], split_line[2], split_line[4], split_line[7]]
                new_line = "\t".join(info)
                with open(output_path + ".txt", "a", encoding="utf-8") as file:
                    file.write(new_line + "\n")

    elif "PaperAuthor" in in_path or "Authors" in in_path:
        dump_dict = dict()
        with open(in_path, "r", encoding="utf-8") as original:
            for line in original:
                split_line = line.split("\t")

                if "PaperAuthor" in in_path:
                    if split_line[0] in dump_dict.keys():
                        dump_dict[split_line[0]].append(split_line[1])
                    else:
                        dump_dict[split_line[0]] = [split_line[1]]

                elif "Authors" in in_path:
                    if split_line[0] in dump_dict.keys():
                        dump_dict[split_line[0]].append(split_line[2])
                    else:
                        dump_dict[split_line[0]] = [split_line[2]]

        with open(output_path + ".json", 'w', encoding="utf-8") as file:
            json.dump(dump_dict, file, sort_keys=True, indent=4)


def find_authors(p_id, pa_dict, au_dict):
    au_info = []
    if p_id in pa_dict.keys():
        au_ids = pa_dict[p_id]
        for au_id in au_ids:
            name = au_dict[au_id][0]
            au_info.append({"n": name, "id": {"mag": int(au_id)}})

    return au_info


def combining_mag_files(ppath, papath, aupath, outpath):
    with open(papath) as pafile:
        padict = json.load(pafile)

        with open(aupath) as aufile:
            audict = json.load(aufile)

            with open(ppath, "r", encoding="utf-8") as pfile:
                for pline in pfile:
                    pinfo = pline.strip('\n').split("\t")
                    pid = pinfo[0]
                    authors = find_authors(pid, padict, audict)
                    new_dict = {"id": {"mag": int(pid)}, "authors": authors, "title": pinfo[2], "year": int(pinfo[3])}
                    if pinfo[1]:
                        new_dict["id"]["doi"] = pinfo[1].lower()
                    with open(outpath, "a", encoding="utf-8") as dfile:
                        json.dump(new_dict, dfile)
                        dfile.write('\n')


def processing_mag_dump(input_dir, output_dir):
    output_path = os.path.join(output_dir, "mag_dump.json")

    # cleaning original mag files
    pa_file = os.path.join(input_dir, "paperauthoraffiliations.json")
    if os.path.exists(pa_file) is False:
        cleaning_mag_file(os.path.join(input_dir, "PaperAuthorAffiliations.txt"))

    au_file = os.path.join(input_dir, "authors.json")
    if os.path.exists(au_file) is False:
        cleaning_mag_file(os.path.join(input_dir, "Authors.txt"))

    p_file = os.path.join(input_dir, "papers.txt")
    if os.path.exists(p_file) is False:
        cleaning_mag_file(os.path.join(input_dir, "Papers.txt"))

    # combining clean mag files
    if os.path.exists(output_path) is False:
        combining_mag_files(p_file, pa_file, au_file, output_path)


def processing_cr_dump(input_dir, output_dir):
    output_path = os.path.join(output_dir, "cr_dump.json")
    if os.path.exists(output_path) is False:

        with os.scandir(input_dir) as json_files:
            for json_file in json_files:
                json_path = os.path.join(input_dir, json_file.name)

                with open(json_path) as file:
                    all_dict = json.load(file)

                    for dd in all_dict["items"]:
                        new_dict = {}

                        if "author" in dd.keys():
                            new_dict["authors"] = []
                            for author in dd["author"]:
                                if "family" in author.keys():
                                    fn = clean_name(author["family"])
                                if "given" in author.keys():
                                    gn = clean_name(author["given"])
                                new_dict["authors"].append({"fn": fn, "gn": gn})

                        if "DOI" in dd.keys():
                            new_dict["id"] = {"doi": dd["DOI"].lower()}

                        if "title" in dd.keys():
                            if dd["title"]:
                                new_dict["title"] = clean_title(dd["title"][0])

                        if "issued" in dd.keys():
                            if "date-parts" in dd["issued"].keys():
                                if dd["issued"]["date-parts"][0][0]:
                                    new_dict["year"] = dd["issued"]["date-parts"][0][0]

                        with open(output_path, "a", encoding="utf-8") as dfile:
                            json.dump(new_dict, dfile)
                            dfile.write('\n')

                print(json_path)


def processing_oa_dump(input_dir, output_dir):
    output_path = os.path.join(output_dir, "oa_dump.json")
    if os.path.exists(output_path) is False:

        with os.scandir(input_dir) as json_files:
            for json_file in json_files:
                json_path = os.path.join(input_dir, json_file.name)

                with open(json_path, encoding="utf-8") as file:
                    for line in file:
                        try:
                            dd = json.loads(line)
                            new_dict = {}

                            if "pid" in dd.keys():
                                for id_dd in dd["pid"]:
                                    if id_dd["scheme"] == "doi" and id_dd["value"]:
                                        new_dict["id"] = {"doi": id_dd["value"].lower()}

                            if "author" in dd.keys():
                                new_dict["authors"] = []
                                for author in dd["author"]:
                                    if "surname" in author.keys():
                                        fn = clean_name(author["surname"])
                                    if "name" in author.keys():
                                        gn = clean_name(author["name"])
                                    new_dict["authors"].append({"fn": fn, "gn": gn})

                            if "maintitle" in dd.keys() and dd["maintitle"]:
                                new_dict["title"] = clean_title(dd["maintitle"])

                            if "publicationdate" in dd.keys() and dd["publicationdate"]:
                                try:
                                    new_dict["year"] = int(dd["publicationdate"][:4])
                                except Exception as ex:
                                    print(repr(ex))
                                    new_dict["year"] = dd["publicationdate"][:4]

                            with open(output_path, "a", encoding="utf-8") as dfile:
                                json.dump(new_dict, dfile)
                                dfile.write('\n')

                        except Exception as ex:
                            print(repr(ex), json_path)

                print(json_path)
