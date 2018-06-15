import importlib as imp
import rdflib
import os
import csv
import config
import people_list

selected_database = config.get_selected_database()

peopleURIs = people_list.get_people_list()

# Prints the count of people retrieved
print("Items count: ", len(peopleURIs))

# Intersection set initialization
propertiesUsageCount = dict()

iterator = 0

current_database_cache_path = "cache/%s/" % selected_database
if not os.path.exists(current_database_cache_path):
    os.makedirs(current_database_cache_path)
listDir = os.listdir(current_database_cache_path)

# Download all the graphs
print("Downloading info...")
for personURI in peopleURIs:
    iterator += 1
    print("%s/%s" % (iterator, len(peopleURIs)))
    try:
        path = personURI.replace("/", "")
        # Downloads all the URIs not already downloaded
        if path not in listDir:
            g = rdflib.Graph()
            g.load(personURI)
            path = current_database_cache_path + path
            g.serialize(destination=path)
    except:
        print("Failed download: %s" % personURI)

iterator = 0

# Count the properties usage
for personURI in listDir:
    iterator += 1
    print("%s/%s\t%s" % (iterator, len(listDir), listDir[iterator - 1]))
    try:
        g = rdflib.Graph()
        g.load(current_database_cache_path + personURI)
        # Counts the usage of the properties
        for _, p, _ in g:
            if p in propertiesUsageCount:
                propertiesUsageCount[p] += 1
            else:
                propertiesUsageCount[p] = 1
    except:
        print("Failed file: %s" % personURI)

# Writes properties usage to csv file
if not os.path.exists("./properties_coverage/"):
    os.makedirs("./properties_coverage/")
with open("./properties_coverage/%s.csv" % selected_database, "w") as f:
    w = csv.writer(f, delimiter=";")
    for key in propertiesUsageCount:
        w.writerow([key, propertiesUsageCount[key], float(propertiesUsageCount[key]) / float(len(listDir))])
