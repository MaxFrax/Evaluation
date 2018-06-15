import xml.etree.ElementTree as ElementTree

def get_people_list():
    # type: () -> list(basestring)

    root = ElementTree.parse("./raw_people_lists/P4169_britishart_yale/P4169_britishart_yale.xml").getroot()
    return list(map(lambda x: x[0][0].text, root[1]))
