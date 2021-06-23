import datetime
from execution_scripts.initialize_execution import *


def coverage_execution(name_cvs_folder, num_cpus):

    print(f'EXTRACT META FROM CVs___________{datetime.datetime.now()}')
    cov_dict = adding_metadata(name_cvs_folder)
    print(datetime.datetime.now())

    cov_years_dict = dict()
    print(f'DOING SEARCHES___________{datetime.datetime.now()}')
    set_searches(cov_dict, num_cpus, cov_years_dict)
    print(datetime.datetime.now())

    print(f'COLLECTING COV BY YEAR___________{datetime.datetime.now()}')
    with open('cov_years_asn.csv', 'w', encoding='utf-8', newline='') as cov_csv:
        writer = csv.writer(cov_csv)
        writer.writerow(("year", "total",
                         "MAG", "OA", "CR", "combined",
                         "MAG%", "OA%", "CR%", "comb%"))

        for year, info in cov_years_dict.items():
            if info["total"] > 0:
                mag_perc = info["mag"] / info["total"]
                oa_perc = info["oa"] / info["total"]
                cr_perc = info["cr"] / info["total"]
                comb_perc = info["comb"] / info["total"]

                writer.writerow((year, info["total"],
                                 info["mag"], info["oa"], info["cr"], info["comb"],
                                 mag_perc, oa_perc, cr_perc, comb_perc))
    print(datetime.datetime.now())

    with open('coverage_asn.csv', 'w', encoding='utf-8', newline='') as cov_csv:
        writer = csv.writer(cov_csv)
        writer.writerow(("term", "role", "field", "id", "total_cv",
                         "MAG", "OA", "CR", "combined",
                         "MAG%", "OA%", "CR%", "comb%"))

        for term, roles in cov_dict['2016'].items():
            for role, fields in roles.items():
                for field, cand_ids in fields.items():
                    for cand_id, cand_dict in cand_ids.items():
                        if 'cov' in cand_dict.keys():
                            info = cand_dict["cov"]
                            if info["total_cv"] > 0:
                                mag_perc = info["mag"] / info["total_cv"]
                                oa_perc = info["oa"] / info["total_cv"]
                                cr_perc = info["cr"] / info["total_cv"]
                                comb_perc = info["comb"] / info["total_cv"]

                                writer.writerow((term, role, field, cand_id, info["total_cv"],
                                                 info["mag"], info["oa"], info["cr"], info["comb"],
                                                 mag_perc, oa_perc, cr_perc, comb_perc))


if __name__ == '__main__':
    name_folder_curriculums = 'cand_cvs'  # change if folder where you stored the candidates' CVs is different
    num_available_cpus = 32
    coverage_execution(name_folder_curriculums, num_available_cpus)
