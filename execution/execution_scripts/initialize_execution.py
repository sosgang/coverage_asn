import ray
from execution_scripts.add_meta import *
from execution_scripts.do_searches import *


def adding_metadata(cvs_folder_name):
    cvs_folder_path = os.path.join(os.getcwd(), cvs_folder_name)
    tsv_path = os.path.join(os.getcwd(), 'execution_scripts', 'indicatoriASN1618.tsv')
    if os.path.exists(os.path.join(os.getcwd(), 'results')) is False:
        os.mkdir(os.path.join(os.getcwd(), 'results'))

    meta_file = os.path.join(os.getcwd(), 'results', 'meta_dict.json')
    if os.path.exists(meta_file) is False:
        meta_dict = dict()
        woinfo_dict = dict()
        finding_metadata(meta_dict, woinfo_dict, tsv_path, cvs_folder_path)

        with open(meta_file, 'w') as meta:
            json.dump(meta_dict, meta, sort_keys=True, indent=2)
        woinfo_file = os.path.join(os.getcwd(), 'results', 'wo_info.json')
        with open(woinfo_file, 'w') as woinfo:
            json.dump(woinfo_dict, woinfo, indent=2)

    else:
        with open(meta_file) as meta:
            meta_dict = json.load(meta)

    return meta_dict


def set_searches(dd, cpus):
    ray.init(num_cpus=cpus, ignore_reinit_error=True)

    folder = os.path.join(os.getcwd(), 'results')

    cache_path = os.path.join(folder, 'cache.json')
    if os.path.exists(cache_path):
        with open(cache_path) as cache_file:
            cache = json.load(cache_file)
    else:
        cache = dict()

    for term, roles in dd['2016'].items():

        if term == "1":
            year_limit = 2017
        elif term == "5":
            year_limit = 2019
        else:
            year_limit = 2018

        term_folder = os.path.join(folder, term)
        if os.path.exists(term_folder) is False:
            os.mkdir(term_folder)

        for role, fields in roles.items():
            role_folder = os.path.join(term_folder, role)
            if os.path.exists(role_folder) is False:
                os.mkdir(role_folder)

            for field, candidates in fields.items():

                field_folder = os.path.join(role_folder, field)
                if os.path.exists(field_folder) is False:
                    with open(cache_path, 'w') as cache_file:
                        json.dump(cache, cache_file, indent=2)
                    os.mkdir(field_folder)

                for cand_id, cand_dict in candidates.items():
                    cand_file = os.path.join(field_folder, f'{cand_id}.json')
                    if os.path.exists(cand_file) is False:
                        if 'pubbs' in cand_dict.keys():
                            search_in_mag(cand_dict, year_limit, cache)  # search in mag for pubbs and by auids
                            search_oa_cr(cand_dict, cache)  # search in oa, cr and count

                            with open(cand_file, 'w') as bib_file:
                                json.dump(cand_dict, bib_file, indent=2)

                    else:
                        with open(cand_file) as bib_file:
                            cand_bib_dict = json.load(bib_file)
                            dd['2016'][term][role][field][cand_id] = cand_bib_dict


def calculating_coverage(info, cov, cov_y_d):
    for pub in info['pubbs']:
        if pub['year'] not in cov_y_d.keys():
            cov_y_d[pub['year']] = {'total': 0, 'mag': 0, 'oa': 0, 'cr': 0, 'comb': 0,
                                    'mag+oa': 0, 'mag+cr': 0, 'oa+cr': 0}
        if 'title' in pub.keys() or 'doi' in pub.keys():
            cov['total_cv'] += 1
            cov_y_d[pub['year']]['total'] += 1
            if 'PId' in pub.keys() or 'oa' in pub.keys() or 'cr' in pub.keys():
                cov['comb'] += 1
                cov_y_d[pub['year']]['comb'] += 1
            if 'PId' in pub.keys() or 'oa' in pub.keys():
                cov['mag+oa'] += 1
                cov_y_d[pub['year']]['mag+oa'] += 1
            if 'PId' in pub.keys() or 'cr' in pub.keys():
                cov['mag+cr'] += 1
                cov_y_d[pub['year']]['mag+cr'] += 1
            if 'oa' in pub.keys() or 'cr' in pub.keys():
                cov['oa+cr'] += 1
                cov_y_d[pub['year']]['oa+cr'] += 1
            if 'PId' in pub.keys():
                cov['mag'] += 1
                cov_y_d[pub['year']]['mag'] += 1
            if 'oa' in pub.keys():
                cov['oa'] += 1
                cov_y_d[pub['year']]['oa'] += 1
            if 'cr' in pub.keys():
                cov['cr'] += 1
                cov_y_d[pub['year']]['cr'] += 1

    return cov


def distinction_cd_nd(s):
    if 1 <= int(s[:2]) <= 9 or s[:4] == "11-E":
        if int(s[:2]) != 8 or s[-2] == "A" or s[-2] == "B":
            # if 1 <= int(s[:2]) < 8 or int(s[:2]) == 9 or s[:4] == "11/E" or s[:4] == "08/A" or s[:4] == "08/B":
            return 'CD'
        else:
            return 'ND'
    else:
        return 'ND'
