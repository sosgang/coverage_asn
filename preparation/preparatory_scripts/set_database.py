import time
import pymongo
import os


def import_dump(db, coll_name, dumps_dir):

    if "mag" in coll_name:
        coll = db.mag
        dump_file = os.path.join(dumps_dir, "mag_dump.json")
    elif "cross" in coll_name:
        coll = db.crossref
        dump_file = os.path.join(dumps_dir, "cr_dump.json")
    elif "open" in coll_name:
        coll = db.openaire
        dump_file = os.path.join(dumps_dir, "oa_dump.json")
    coll.insert_many(dump_file)


def create_indexes(db, coll_name):
    start = 0
    end = 0

    if "mag" in coll_name:
        mag = db.mag

        start = time.time()
        mag.create_index([('year', pymongo.ASCENDING), ("title", pymongo.TEXT)],
                         name="YTi", background=True, sparse=True, default_language='none')
        mag.create_index([("id.doi", pymongo.ASCENDING)], name='Doi', background=True)
        mag.create_index([("id.mag", pymongo.ASCENDING)], name='PId', background=True)
        mag.create_index([("authors.id.mag", pymongo.ASCENDING)], name='AuId', background=True)
        end = time.time()

    elif "cross" in coll_name or "open" in coll_name:
        if "cross" in coll_name:
            coll = db.crossref
        elif "open" in coll_name:
            coll = db.openaire

        start = time.time()
        coll.create_index([('year', pymongo.ASCENDING), ("title", pymongo.TEXT)],
                          name="YTi", background=True, sparse=True, default_language='none')
        coll.create_index([("id.doi", pymongo.ASCENDING)], name='Doi', background=True)
        end = time.time()

    print(f"Time to create indexes for {coll_name} collection: ", end - start)
