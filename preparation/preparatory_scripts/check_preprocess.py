import os
import subprocess
import tarfile


def check_number_docs(og_dir, mag_dir, cr_dir, oa_dir, final_dir):

# CHECK OPENAIRE FILES
    dump_n_files = 0
    for n in range(1, 10):
        part_oa_dump = tarfile.open(os.path.join(os.getcwd(), og_dir, f'publication_{n}.tar'), 'r')
        part_files_list = part_oa_dump.getmembers()
        dump_n_files += len(part_files_list)
    extr_files_list = [f for f in os.listdir(os.path.join(os.getcwd(), oa_dir))]
    extr_n_files = len(extr_files_list)
    print(f'OPENAIRE num files: compressed {dump_n_files}, extracted {extr_n_files}')

    extr_n_rows = 0
    for f in extr_files_list:
        res = subprocess.run(['wc', '-l', os.path.join(os.getcwd(), oa_dir, f)],
                             stdout=subprocess.PIPE).stdout.decode('utf-8')
        n_rows = int(res.split(' ')[0])
        extr_n_rows += n_rows
    res1 = subprocess.run(['wc', '-l', os.path.join(os.getcwd(), final_dir, 'oa_dump.json')],
                          stdout=subprocess.PIPE).stdout.decode('utf-8')
    prssd_n_rows = int(res1.split(' ')[0])
    print(f'OPENAIRE num rows: extracted {extr_n_rows}, processed {prssd_n_rows}')


# CHECK CROSSREF FILES
    cr_dump = tarfile.open(os.path.join(os.getcwd(), og_dir, 'crossref.tar.gz'), 'r:gz')
    dump_files_list = cr_dump.getmembers()
    dump_n_files = len(dump_files_list)
    extr_files_list = [f for f in os.listdir(os.path.join(os.getcwd(), cr_dir))]
    extr_n_files = len(extr_files_list)
    print(f'CROSSREF num files: compressed {dump_n_files}, extracted {extr_n_files}')

    extr_n_rows = 0
    for f in extr_files_list:
        res = subprocess.run(['wc', '-l', os.path.join(os.getcwd(), cr_dir, f)],
                             stdout=subprocess.PIPE).stdout.decode('utf-8')
        n_rows = int(res.split(' ')[0]) - 2
        extr_n_rows += n_rows
    res1 = subprocess.run(['wc', '-l', os.path.join(os.getcwd(), final_dir, 'cr_dump.json')],
                          stdout=subprocess.PIPE).stdout.decode('utf-8')
    prssd_n_rows = int(res1.split(' ')[0])
    print(f'CROSSREF num rows: extracted {extr_n_rows}, processed {prssd_n_rows}')


# CHECK MAG FILES
    res = subprocess.run(['wc', '-l', os.path.join(os.getcwd(), mag_dir, 'Papers.txt')],
                         stdout=subprocess.PIPE).stdout.decode('utf-8')
    extr_n_rows = int(res.split(' ')[0])
    res1 = subprocess.run(['wc', '-l', os.path.join(os.getcwd(), final_dir, 'mag_dump.json')],
                          stdout=subprocess.PIPE).stdout.decode('utf-8')
    prssd_n_rows = int(res1.split(' ')[0])
    print(f'MAG num rows: extracted {extr_n_rows}, processed {prssd_n_rows}')
