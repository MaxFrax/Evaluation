import xml.etree.cElementTree as ElementTree
import rdflib
import os
import csv

# Transforming xml from yale to a list of people URIs
root = ElementTree.parse("./people_lists/P4169_britishart_yale.xml").getroot()

peopleURIs = list(map(lambda x: x[0][0].text, root[1]))

# Prints the count of people retrieved
print "Items count: ", len(peopleURIs)

# Intersection set initialization
propertiesUsageCount = dict()

iterator = 0

if not os.path.exists("./cache/P4169_britishart_yale"):
    os.makedirs("./cache/P4169_britishart_yale")
listDir = os.listdir("./cache/P4169_britishart_yale")

# Download all the graphs
print "Downloading info..."
for personURI in peopleURIs:
    iterator += 1
    print "%s/%s" % (iterator, len(peopleURIs))
    try:
        path = personURI.replace("/", "")
        # Downloads all the URIs not already downloaded
        if path not in listDir:
            g = rdflib.Graph()
            g.load(personURI)
            path = "cache/P4169_britishart_yale/" + path
            g.serialize(destination=path)
    except:
        print "Failed download: %s" % personURI

iterator = 0

# Count the properties usage
for personURI in listDir:
    iterator += 1
    print "%s/%s\t%s" % (iterator, len(listDir), listDir[iterator - 1])
    try:
        g = rdflib.Graph()
        g.load("cache/P4169_britishart_yale/" + personURI)
        # Counts the usage of the properties
        for _, p, _ in g:
            if p in propertiesUsageCount:
                propertiesUsageCount[p] += 1
            else:
                propertiesUsageCount[p] = 1
    except:
        print "Failed file: %s" % personURI

# Writes properties usage to csv file
if not os.path.exists("./properties_coverage/"):
    os.makedirs("./properties_coverage/")
with open("./properties_coverage/P4169_britishart_yale.csv", "wb") as f:
    w = csv.writer(f, delimiter=";")
    for key in propertiesUsageCount:
        w.writerow([key, propertiesUsageCount[key], float(propertiesUsageCount[key]) / float(len(listDir))])
