import pymongo
import ray


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


def check_authors(cv_authors, r_authors, key):
    idx_au = 0
    n_au = len(cv_authors)
    n_rau = len(r_authors)
    found = 0
    goal = round(n_au * 0.6)
    while idx_au < n_au:
        idx_rau = 0
        while idx_rau < n_rau:
            if r_authors[idx_rau][key] and cv_authors[idx_au]:
                if key == 'n':
                    fn = r_authors[idx_rau][key].split(' ')[-1]
                elif key == 'fn':
                    fn = r_authors[idx_rau][key]
                if fn in cv_authors[idx_au]:
                    found += 1
                    if found == goal:
                        return 1
            idx_rau += 1
        idx_au += 1
    return 0


@ray.remote
def search_title_mag(title_wostop, year, authors):
    client = pymongo.MongoClient()
    db = client.bond_cov
    mag = db.mag

    results = mag.find({'year': year, '$text': {'$search': title_wostop}}, {'score': {'$meta': 'textScore'}}).limit(50)
    for r in results.sort([('score', {'$meta': 'textScore'})]):
        if 'authors' in r.keys() and len(authors)-2 < len(r['authors']) < len(authors)+2:
            au_found = check_authors(authors, r['authors'], 'n')
            if au_found:
                doi = ''
                if 'id' in r.keys() and "doi" in r['id'].keys():
                    doi = r['id']['doi']
                return [r['id']['mag'], doi, r['authors']]


@ray.remote
def search_title_oa(title_wostop, year, authors):
    client = pymongo.MongoClient()
    db = client.bond_cov
    oa = db.openaire

    results = oa.find({'year': year, '$text': {'$search': title_wostop}}, {'score': {'$meta': 'textScore'}}).limit(50)
    for r in results.sort([('score', {'$meta': 'textScore'})]):
        if 'authors' in r.keys() and len(authors)-2 < len(r['authors']) < len(authors)+2:
            au_found = check_authors(authors, r['authors'], 'fn')
            if au_found:
                doi = ''
                if 'id' in r.keys() and "doi" in r['id'].keys():
                    doi = r['id']['doi']
                return doi


@ray.remote
def search_title_cr(title_wostop, year, authors):
    client = pymongo.MongoClient()
    db = client.bond_cov
    cr = db.crossref

    results = cr.find({'year': year, '$text': {'$search': title_wostop}}, {'score': {'$meta': 'textScore'}}).limit(50)
    for r in results.sort([('score', {'$meta': 'textScore'})]):
        if 'authors' in r.keys() and len(authors)-2 < len(r['authors']) < len(authors)+2:
            au_found = check_authors(authors, r['authors'], 'fn')
            if au_found:
                doi = ''
                if 'id' in r.keys() and "doi" in r['id'].keys():
                    doi = r['id']['doi']
                return doi


def search_doi_mag(doi):
    client = pymongo.MongoClient()
    db = client.bond_cov
    mag = db.mag
    results = mag.find({"id.doi": doi})
    for r in results:
        return [r['id']['mag'], r['authors']]


def search_doi_oa(doi):
    client = pymongo.MongoClient()
    db = client.bond_cov
    oa = db.openaire
    results = oa.find({"id.doi": doi})
    if list(results):
        return 1


def search_doi_cr(doi):
    client = pymongo.MongoClient()
    db = client.bond_cov
    cr = db.crossref
    results = cr.find({"id.doi": doi})
    if list(results):
        return 1


def search_auid(date, au_id, pubbs):
    client = pymongo.MongoClient()
    db = client.bond_cov
    mag = db.mag
    results = mag.find({"authors.id.mag": au_id, 'year': {'$lt': date}})
    for r in results:
        n = len(pubbs)
        idx = 0
        while idx < n:
            if "PId" in pubbs[idx].keys() and r["id"]["mag"] == pubbs[idx]["PId"]:
                    idx = n
            elif "doi" in r['id'].keys() and "doi" in pubbs[idx].keys():
                if r["id"]["doi"] == pubbs[idx]["doi"]:
                    pubbs[idx]["PId"] = r["id"]["mag"]
                    idx = n
            elif "title" in pubbs[idx].keys():
                new_title = r["title"].replace(' ', '')
                old_title = pubbs[idx]["title"].replace(' ', '')
                l_new = len(new_title)
                l_old = len(old_title)
                new_year = r["year"]
                old_year = pubbs[idx]["year"]
                if l_old >= l_new:
                    if new_title == old_title[:l_new] and old_year - 2 <= new_year <= old_year + 2:
                        pubbs[idx]["PId"] = r["id"]["mag"]
                        if "doi" in r.keys():
                            pubbs[idx]["doi"] = r["id"]["doi"]
                        idx = n
                    elif new_title == old_title[-l_new:] and old_year - 2 <= new_year <= old_year + 2:
                        pubbs[idx]["PId"] = r["id"]["mag"]
                        if "doi" in r.keys():
                            pubbs[idx]["doi"] = r["id"]["doi"]
                        idx = n
                else:
                    if new_title[:l_old] == old_title and old_year - 2 <= new_year <= old_year + 2:
                        pubbs[idx]["PId"] = r["id"]["mag"]
                        if "doi" in r.keys():
                            pubbs[idx]["doi"] = r["id"]["doi"]
                        idx = n
                    elif new_title[-l_old:] == old_title and old_year - 2 <= new_year <= old_year + 2:
                        pubbs[idx]["PId"] = r["id"]["mag"]
                        if "doi" in r.keys():
                            pubbs[idx]["doi"] = r["id"]["doi"]
                        idx = n

            idx += 1
