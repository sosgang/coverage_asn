import datetime
from execution_scripts.initialize_execution import *


def coverage_execution(name_cvs_folder, num_cpus):
    print(f'EXTRACT META FROM CVs___________{datetime.datetime.now()}')
    cov_dict = adding_metadata(name_cvs_folder)

    print(f'DOING SEARCHES___________{datetime.datetime.now()}')
    set_searches(cov_dict, num_cpus)

    print(f'CALCULATING COVERAGE___________{datetime.datetime.now()}')
    cov_years_dict = dict()
    cov_cand_csv = open('cov_asn_xcand.csv', 'w', encoding='utf-8', newline='')
    cand_cov_writer = csv.writer(cov_cand_csv)
    cand_cov_writer.writerow(("term", "role", "SA", "field", "field_type", "id", "total_cv",
                              "MAG", "MAG%", "OA", "OA%", "CR", "CR%",
                              "MAG+OA", "MAG+OA%", "MAG+CR", "MAG+CR%",
                              "OA+CR", "OA+CR%", "Comb", "Comb%",))

    cov_dataset_csv = open('cov_asn_xdataset.csv', 'w', encoding='utf-8', newline='')
    dataset_cov_writer = csv.writer(cov_dataset_csv)
    dataset_cov_writer.writerow(("dataset", "term", "role", "SA", "field", "field_type", "coverage%"))

    print(f'COV BY CANDIDATE AND DATASET___________{datetime.datetime.now()}')
    for root, subdirectories, files in os.walk('results'):
        for filename in files:
            if 'DS_' not in filename and 'info' not in filename and 'cache' not in filename and 'dict' not in filename:
                with open(os.path.join(root, filename)) as cand_file:
                    cand = json.load(cand_file)
                    cov = {'total_cv': 0, 'mag': 0, 'oa': 0, 'cr': 0, 'comb': 0,
                           'mag+oa': 0, 'mag+cr': 0, 'oa+cr': 0}
                    calculating_coverage(cand, cov, cov_years_dict)
                    term = cand['cv_id'][1]
                    role = cand['cv_id'][2]
                    field = cand['cv_id'][3]
                    field_type = distinction_cd_nd(field)
                    field_clean = field.replace("-", "/")+f' ({field_type})'
                    sa = str(field_clean[:2])
                    cand_id = cand['cv_id'][4]
                    if cov["total_cv"] > 0:
                        mag_perc = cov["mag"] / cov["total_cv"]
                        oa_perc = cov["oa"] / cov["total_cv"]
                        cr_perc = cov["cr"] / cov["total_cv"]
                        magoa_perc = cov['mag+oa']/cov['total_cv']
                        magcr_perc = cov['mag+cr']/cov['total_cv']
                        oacr_perc = cov['oa+cr']/cov['total_cv']
                        comb_perc = cov["comb"] / cov["total_cv"]

                        cand_cov_writer.writerow((term, role, sa, field_clean, field_type, cand_id, cov["total_cv"],
                                                  cov["mag"], mag_perc, cov["oa"], oa_perc, cov["cr"], cr_perc,
                                                  cov['mag+oa'], magoa_perc, cov['mag+cr'], magcr_perc,
                                                  cov['oa+cr'], oacr_perc, cov["comb"], comb_perc))

                        dataset_cov_writer.writerow(("MAG", term, role, sa, field_clean, field_type, mag_perc))
                        dataset_cov_writer.writerow(("OA", term, role, sa, field_clean, field_type, oa_perc))
                        dataset_cov_writer.writerow(("CR", term, role, sa, field_clean, field_type, cr_perc))
                        dataset_cov_writer.writerow(("MAG+OA", term, role, sa, field_clean, field_type, magoa_perc))
                        dataset_cov_writer.writerow(("MAG+CR", term, role, sa, field_clean, field_type, magcr_perc))
                        dataset_cov_writer.writerow(("OA+CR", term, role, sa, field_clean, field_type, oacr_perc))
                        dataset_cov_writer.writerow(("Comb", term, role, sa, field_clean, field_type, comb_perc))

    cov_cand_csv.close()
    cov_dataset_csv.close()

    print(f'COV BY YEAR___________{datetime.datetime.now()}')
    sorted_y_dict = sorted(cov_years_dict.items())
    with open('cov_asn_xyear.csv', 'w', encoding='utf-8', newline='') as cov_csv:
        writer = csv.writer(cov_csv)
        writer.writerow(("year", "total",
                         "MAG", "MAG%", "OA", "OA%", "CR", "CR%",
                         "MAG+OA", "MAG+OA%", "MAG+CR", "MAG+CR%",
                         "OA+CR", "OA+CR%", "Comb", "Comb%"))
        for tuple in sorted_y_dict:
            year = tuple[0]
            info = tuple[1]
            if info["total"] > 0:
                mag_perc = info["mag"] / info["total"]
                oa_perc = info["oa"] / info["total"]
                cr_perc = info["cr"] / info["total"]
                magoa_perc = info['mag+oa'] / info['total']
                magcr_perc = info['mag+cr'] / info['total']
                oacr_perc = info['oa+cr'] / info['total']
                comb_perc = info["comb"] / info["total"]

                writer.writerow((year, info["total"],
                                 info["mag"], mag_perc, info["oa"], oa_perc, info["cr"], cr_perc,
                                 info["mag+oa"], magoa_perc, info["mag+cr"], magcr_perc,
                                 info["oa+cr"], oacr_perc, info["comb"], comb_perc))


if __name__ == '__main__':
    name_folder_curriculums = 'cand_cvs'  # change if folder where you stored the candidates' CVs is different
    num_available_cpus = 32
    coverage_execution(name_folder_curriculums, num_available_cpus)
