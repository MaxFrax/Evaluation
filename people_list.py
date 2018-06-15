# Checks if the standard format people list is stored for the selected database
# If it's not existing, imports the module form the raw list, gets the list, stores it
# return the list to the main module which called this module
from typing import TextIO

import config
import os.path
import importlib as imp

selected_database = config.get_selected_database()
people_list_folder_path = "people_lists/"
people_list_path = "%s%s.txt" % (people_list_folder_path, selected_database)


# TODO optimize:
# if the list is written when the function is called you could return the value without interacting with disk
def get_people_list():
    if not os.path.exists(people_list_folder_path):
        os.makedirs(people_list_folder_path)
    if not os.path.isfile(people_list_path):
        _write_list()
    return _read_list()


def _write_list():
    database = imp.import_module("raw_people_lists.%s.getter" % selected_database)
    people_uris = database.get_people_list()
    with open(people_list_path, "w") as ppl:
        ppl.writelines("%s\n" % uri for uri in people_uris)


def _read_list():
    with open(people_list_path, "r") as ppl:
        return [item.replace("\n", "") for item in ppl.readlines()]
