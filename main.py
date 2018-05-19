import xml.etree.cElementTree as ElementTree
import rdflib
import os
import csv

# Transforming xml from yale to a list of people URIs
root = ElementTree.parse("person-list.xml").getroot()

peopleURIs = list(map(lambda x: x[0][0].text, root[1]))

# Prints the count of people retrieved
print "Items count: ", len(peopleURIs)

# Intersection set initialization
propertiesUsageCount = dict()

iterator = 0
listDir = os.listdir("./Yale-Data")

# Download all the graphs
print "Downloading info..."
for personURI in peopleURIs:
    iterator += 1
    print "%s/%s" % (iterator, len(peopleURIs))
    path = personURI.replace("/", "")
    # Downloads all the URIs not already downloaded
    if path not in listDir:
        g = rdflib.Graph()
        g.load(personURI)
        path = "Yale-Data/" + path
        g.serialize(destination=path)

iterator = 0

with open("people.csv", "wb") as f:
    w = csv.writer(f, delimiter=";")

    for personURI in listDir:
        iterator += 1
        print "%s/%s\t%s" % (iterator, len(listDir), listDir[iterator - 1])
        try:
            g = rdflib.Graph()
            g.load("Yale-Data/" + personURI)
            # Counts the usage of the properties
            for _, p, _ in g:
                if p in propertiesUsageCount:
                    propertiesUsageCount[p] += 1
                else:
                    propertiesUsageCount[p] = 1
        except:
            print "Failed file: %s" % personURI

        queryResult = g.query("""SELECT ?id ?fullName ?gender ?birth ?death ?nationality
    WHERE {
    ?id <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://erlangen-crm.org/current/E21_Person> .
    ?id <http://www.w3.org/2004/02/skos/core#altLabel> ?fullname .
    OPTIONAL { ?id <http://collection.britishmuseum.org/id/ontology/PX_gender> ?gender } .
    OPTIONAL { ?id <http://erlangen-crm.org/current/P98i_was_born> ?birth } .
    OPTIONAL { ?id <http://erlangen-crm.org/current/P100i_died_in> ?death } .
    OPTIONAL { ?id <http://collection.britishmuseum.org/id/ontology/PX_nationality> ?nationality }
    }""")
        for result in queryResult:
            w.writerow(result)

# Writes properties usage to csv file
with open("propertiesUsageCount.csv", "wb") as f:
    w = csv.writer(f, delimiter=";")
    for key in propertiesUsageCount:
        w.writerow([key, propertiesUsageCount[key]])
