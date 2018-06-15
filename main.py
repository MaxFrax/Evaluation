import cache

cache.download_people_list()


# Count the properties usage
# for personURI in listDir:
#     iterator += 1
#     print("%s/%s\t%s" % (iterator, len(listDir), listDir[iterator - 1]))
#     try:
#         g = rdflib.Graph()
#         g.load(current_database_cache_path + personURI)
#         # Counts the usage of the properties
#         for _, p, _ in g:
#             if p in propertiesUsageCount:
#                 propertiesUsageCount[p] += 1
#             else:
#                 propertiesUsageCount[p] = 1
#     except:
#         print("Failed file: %s" % personURI)
#
# # Writes properties usage to csv file
# if not os.path.exists("./properties_coverage/"):
#     os.makedirs("./properties_coverage/")
# with open("./properties_coverage/%s.csv" % selected_database, "w") as f:
#     w = csv.writer(f, delimiter=";")
#     for key in propertiesUsageCount:
#         w.writerow([key, propertiesUsageCount[key], float(propertiesUsageCount[key]) / float(len(listDir))])
