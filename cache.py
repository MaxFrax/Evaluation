# Checks foreach uri in the list there is a stored copy of it
import config
import os.path
import people_list
import rdflib

selected_database = config.get_selected_database()
cache_folder_path = "cache/"
database_cache_path = "%s%s/" % (cache_folder_path, selected_database)


def download_people_list():
    _check_folder_existence()

    cached_items = set(os.listdir(database_cache_path))
    people_uris = people_list.get_people_list()

    for person_uri in people_uris:
        person_uri_cleaned = person_uri.replace("/", "_")
        person_path = "%s%s" % (database_cache_path, person_uri_cleaned)

        if person_uri_cleaned not in cached_items:
            g = rdflib.Graph()
            g.load(person_uri)
            g.serialize(person_path)


def get_people_paths():
    _check_folder_existence()
    people = os.listdir(database_cache_path)
    return ["%s%s" % (database_cache_path, person) for person in people]


def _check_folder_existence():
    if not os.path.exists(cache_folder_path):
        os.makedirs(cache_folder_path)
    if not os.path.exists(database_cache_path):
        os.makedirs(database_cache_path)
