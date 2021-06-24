from preparatory_scripts import process_dumps
from preparatory_scripts import check_dump_process
from preparatory_scripts import set_database
import os
import pymongo


def processing(originals_dir, input_mag_dir, input_cr_dir, input_oa_dir, output_dir):

    process_dumps.processing_mag_dump(input_mag_dir, output_dir)
    process_dumps.processing_cr_dump(input_cr_dir, output_dir)
    process_dumps.processing_oa_dump(input_oa_dir, output_dir)

    # check if any files or publications from the original dump have been lost in the process
    check_dump_process.check_number_docs(originals_dir, input_mag_dir, input_cr_dir, input_oa_dir, output_dir)


def importing_dumps_to_db(output_dir):

    client = pymongo.MongoClient()
    database = client.coverage_asn
    for collection_name in ["mag", "crossref", "openaire"]:
        set_database.import_dump(database, collection_name, output_dir)

    client.close()


def create_indexes_in_db():

    client = pymongo.MongoClient()
    database = client.coverage_asn
    for collection_name in ["mag", "crossref", "openaire"]:
        set_database.create_indexes(database, collection_name)

    client.close()


if __name__ == '__main__':
    originals_dir = os.path.join(os.getcwd(), "originals")  # name of the folder with original compressed files
    input_mag_dir = os.path.join(os.getcwd(), "mag")        # name of the folder with mag original decompressed txt files
    input_cr_dir = os.path.join(os.getcwd(), "crossref")    # name of the folder with crossref original decompressed json files
    input_oa_dir = os.path.join(os.getcwd(), "openaire")    # name of the folder with openaire original decompressed json files
    output_dir = os.path.join(os.getcwd(), "final")

    # it won't process dumps if there is a folder named "final" in your working directory
    # you can download the final folder with the processed dumps from zenodo
    if os.path.exists(output_dir) is False:
        os.mkdir(output_dir)
        processing(originals_dir, input_mag_dir, input_cr_dir, input_oa_dir, output_dir)

    importing_dumps_to_db(output_dir)  # comment out if you do not need to import the dumps' data to your database

    create_indexes_in_db()  # comment out if you do not need to create indexes in your database
