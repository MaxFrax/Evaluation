import cache
import rdflib
import os.path
import config
import csv

selected_database = config.get_selected_database()
properties_coverage_folder = "properties_coverage/"


def compute_properties_coverage():
    people_paths = cache.get_people_paths()
    properties_usage_count = dict()

    for person_path in people_paths:
        try:
            g = rdflib.Graph()
            g.load(person_path)
            # Counts the usage of the properties
            for _, p, _ in g:
                if p in properties_usage_count:
                    properties_usage_count[p] += 1
                else:
                    properties_usage_count[p] = 1
        except:
            print("Failed file: %s" % person_path)
    _write_coverage_csv(properties_usage_count, len(people_paths))


def _write_coverage_csv(properties_usage_count, total_people_count):
    _check_folder_existence()
    with open("%s%s.csv" % (properties_coverage_folder, selected_database), "w") as f:
        w = csv.writer(f, delimiter=";")
        for key in properties_usage_count:
            w.writerow([key, properties_usage_count[key], float(properties_usage_count[key]) / float(total_people_count)])


def _check_folder_existence():
    if not os.path.exists(properties_coverage_folder):
        os.makedirs(properties_coverage_folder)
