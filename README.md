# Evaluation
This piece of software helps to evaluate rdf datasources to understand the converage of the attributes over a set of given entities.  
The entities must be expressed as valid URIs.

This code is meant to support the development of [soweego](https://meta.wikimedia.org/wiki/Grants:Project/Hjfocs/soweego). 

## Technologies
- Python 3.6.5
- [rdflib](https://github.com/RDFLib/rdflib)

## Get started
1. Download [PyCharm](https://www.jetbrains.com/pycharm/download/)
1. Download this repository
1. Open this repository as PyCharm project with PyCharm
1. Get a *whatever format* list of entities URI
1. Give to that file a smart name (not mandatory)
1. Create a folder with the **same name of the list file** inside `raw_people_lists`
1. Put the list inside the folder you have just created
1. Inside the folder create a file `__init__.py`
1. Create also a `getter.py` file
1. In `getter.py` define `get_people_list()`.  
This function must return a list of valid URI strings created from your raw list.
1. Put the file name into `config.py`
1. Run `main.py`

## Project Architecture (from usage standpoint)
Project entry point: `main.py`  
Data source selection: `config.py`

### 1. Raw entities list
Is the first state of the process.  
Basically you give a whatever format list, with valid URIs.

With a dynamic module loading architecture, you define how your file format becomes a list of URI strings.  
The definition is given by you into `getter.py`, as described in **Getting Started**.

### 2. Common format entities list
This step happens inside `people_list.py`, it's triggered calling `get_people_list()`.  
Basically from it reads from the `config.py` which `getter.py` module should be dinamically loaded.  
Once loaded calls `getter.get_people_list()` and stores the common format list into `people_lists` folder. (to avoid useless computation in next runs)  
All this stuff is done only if there is no list stored for the selected data source.

## TODO
• Improve feedback on what's happening while the script is executing