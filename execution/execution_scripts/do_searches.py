import ray
from execution_scripts.search_kinds import *


def remove_stopwords(title):
    stoplist = [line.strip() for line in open('stoplist_final.txt')]
    stoplist = set(stoplist)
    keywords = [w for w in title.split(' ') if w and w not in stoplist]
    wostop = ' '.join(keywords[:5])

    return wostop


def identify_author_mag(cv_fullname, r_authors):
    last_fn = cv_fullname[0].split(' ')[-1]
    first_gn = cv_fullname[1].split(' ')[0]
    possible_aus = []

    for author in r_authors:
        if cv_fullname[0] in author['n'] or last_fn in author['n']:
            possible_aus.append((author['id']['mag'], author['n']))

    if len(possible_aus) == 1:
        return possible_aus[0][0]

    if len(possible_aus) > 1:
        for possible_au in possible_aus:
            if first_gn in possible_au[1]:
                return possible_au[0]


def check_cache_results(possible_results, cv_fn):
    for possible_res in possible_results:  # for possible result with same year and keywords
        for possible_fn in possible_res[0]:  # for au in possible result
            if cv_fn in possible_fn or possible_fn in cv_fn:  # if possible_fn in candidate's fullname
                result = possible_res[1]  # use the existing result
                return result

    return 404


def search_in_mag(info, y_limit, ch):
    futures = []
    pubbs_idx = []
    auids = set()
    for pub in info['pubbs']:
        if 'doi' in pub.keys():
            result = search_doi_mag(pub['doi'])
            if result is not None:
                if result[0]:
                    pub['PId'] = result[0]
                if result[1]:
                    auid = identify_author_mag(info['fullname'], result[1])
                    auids.add(auid)

        elif 'title' in pub.keys():
            year = pub['year']
            title_wostop = remove_stopwords(pub['title'])
            chkey = f'{year}_{title_wostop}'

            if chkey in ch.keys() and 'mag' in ch[chkey].keys():  # check if result in cache first
                result = check_cache_results(ch[chkey]['mag'], info['fullname'][0])
                if result != 404:
                    if result is not None:
                        if result[0]:
                            pub['PId'] = result[0]
                        if result[1]:
                            pub['doi'] = result[1]
                        if result[2]:
                            auid = identify_author_mag(info['fullname'], result[2])
                            auids.add(auid)
                else:
                    futures.append(search_title_mag.remote(title_wostop, year, pub['authors']))
                    pubbs_idx.append(pub['pub_idx'])
            else:
                futures.append(search_title_mag.remote(title_wostop, year, pub['authors']))
                pubbs_idx.append(pub['pub_idx'])

    results = ray.get(futures)
    idx = 0
    while idx < len(results):
        result = results[idx]  # position of result in list of obtained results
        pub_idx = pubbs_idx[idx]  # position of related publication in cand dict
        pub = info['pubbs'][pub_idx]  # publication
        year = pub['year']
        title_wostop = remove_stopwords(pub['title'])
        chkey = f'{year}_{title_wostop}'
        if chkey not in ch.keys():
            ch[chkey] = dict()
        if 'mag' not in ch[chkey].keys():
            ch[chkey]['mag'] = []
        ch[chkey]['mag'].append([pub['authors'], result])  # adding search info and result to cache
        if result is not None:
            if result[0]:
                pub['PId'] = result[0]
            if result[1]:
                pub['doi'] = result[1]
            if result[2]:
                auid = identify_author_mag(info['fullname'], result[2])
                auids.add(auid)
        idx += 1

    info['AuIds'] = list(auids)
    for au_id in info['AuIds']:
        search_auid(y_limit, au_id, info['pubbs'])

    return info


def search_oa_cr(info, ch):
    futures_oa = []
    pubbs_idx_oa = []
    futures_cr = []
    pubbs_idx_cr = []
    for pub in info['pubbs']:
        if 'doi' in pub.keys():
            res_oa = search_doi_oa(pub['doi'])
            if res_oa:
                pub['oa'] = 1
            res_cr = search_doi_cr(pub['doi'])
            if res_cr:
                pub['cr'] = 1
        elif 'title' in pub.keys():
            year = pub['year']
            title_wostop = remove_stopwords(pub['title'])
            chkey = f'{year}_{title_wostop}'

            if chkey in ch.keys() and 'oa' in ch[chkey].keys():
                res_oa = check_cache_results(ch[chkey]['oa'], info['fullname'][0])
                if res_oa != 404:
                    if res_oa is not None:
                        pub['oa'] = 1
                        if res_oa:
                            pub['doi'] = res_oa
                else:
                    futures_oa.append(search_title_oa.remote(title_wostop, year, pub['authors']))
                    pubbs_idx_oa.append(pub['pub_idx'])
            else:
                futures_oa.append(search_title_oa.remote(title_wostop, year, pub['authors']))
                pubbs_idx_oa.append(pub['pub_idx'])

            if chkey in ch.keys() and 'cr' in ch[chkey].keys():
                res_cr = check_cache_results(ch[chkey]['cr'], info['fullname'][0])
                if res_cr != 404:
                    if res_cr is not None:
                        pub['cr'] = 1
                        if res_cr:
                            pub['doi'] = res_cr
                else:
                    futures_cr.append(search_title_cr.remote(title_wostop, year, pub['authors']))
                    pubbs_idx_cr.append(pub['pub_idx'])
            else:
                futures_cr.append(search_title_cr.remote(title_wostop, year, pub['authors']))
                pubbs_idx_cr.append(pub['pub_idx'])

    results_oa = [r for r in ray.get(futures_oa)]
    idx = 0
    while idx < len(results_oa):
        res_oa = results_oa[idx]  # position of result in list of obtained results
        pub_idx = pubbs_idx_oa[idx]  # position of related publication in cand dict
        pub = info['pubbs'][pub_idx]  # publication
        year = pub['year']
        title_wostop = remove_stopwords(pub['title'])
        chkey = f'{year}_{title_wostop}'
        if chkey not in ch.keys():
            ch[chkey] = dict()
        if 'oa' not in ch[chkey].keys():
            ch[chkey]['oa'] = []
        ch[chkey]['oa'].append([pub['authors'], res_oa])    # adding search info as key, and search result as value, to cache
        if res_oa is not None:
            pub['oa'] = 1
            if res_oa:
                pub['doi'] = res_oa
        idx += 1

    results_cr = [r for r in ray.get(futures_cr)]
    idx = 0
    while idx < len(results_cr):
        res_cr = results_cr[idx]  # position of result in list of obtained results
        pub_idx = pubbs_idx_cr[idx]  # position of related publication in cand dict
        pub = info['pubbs'][pub_idx]  # publication
        year = pub['year']
        title_wostop = remove_stopwords(pub['title'])
        chkey = f'{year}_{title_wostop}'
        if chkey not in ch.keys():
            ch[chkey] = dict()
        if 'cr' not in ch[chkey].keys():
            ch[chkey]['cr'] = []
        ch[chkey]['cr'].append([pub['authors'], res_cr])    # adding search info as key, and search result as value, to cache
        if res_cr is not None:
            pub['cr'] = 1
            if res_cr:
                pub['doi'] = res_cr
        idx += 1
