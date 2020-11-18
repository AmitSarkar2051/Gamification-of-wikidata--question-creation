import sys
from SPARQLWrapper import SPARQLWrapper, JSON
import random
import os
import shutil

#global vars
dataFolder="chem_folder/"
endpoint_url = "https://query.wikidata.org/sparql"
query_getelements = """SELECT ?item ?itemLabel 
WHERE 
{
  ?item wdt:P31 wd:Q11344.
  SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
}"""

#required  utils
def create_newAllPropFile(myList):
    print("Writing in the file. . ..ALL_English_proplist_v2.txt")
    print("Available size", len(myList))
    with open('ALL_English_proplist_v2.txt', 'w') as f:
        for item in myList:
            f.write("%s\n" % item)

def create_newPropFile(myList):
    with open('tmp_English_proplist.txt', 'w') as f:
        for item in myList:
            f.write("%s\n" % item)

def show(myList):
    for x in myList:
        print(x)

def extract_results(url,query):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(url, agent=user_agent)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def main():
    print("English Create property-map program started . . .")
    all_elements=[]
    tmplist=[]
    results = extract_results(endpoint_url, query_getelements)
    All_en=[]
    All_en_dict={}
    for result in results["results"]["bindings"]:
        all_elements.append(result['item']['value'].split('/')[-1])

    for i in range(len(all_elements)):
        query_getproperty = """SELECT ?wdLabel {
	    VALUES (?element) {(wd:"""+str(all_elements[i])+""")}
	    ?element ?p ?statement .
	    ?wd wikibase:claim ?p.
	    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
	    } ORDER BY ?wd ?statement ?ps_"""
        
        propList = extract_results(endpoint_url, query_getproperty)
        for result in propList["results"]["bindings"]:
            All_en_dict[result['wdLabel']['value']] = 1
            All_en.append(result['wdLabel']['value'])

        for result in propList["results"]["bindings"]:
            if result['wdLabel']['value'][0] == 'P':
                tmplist.append(result['wdLabel']['value'])

    #tmplist.sort()
    propSet=set(tmplist)
    print("Number of unnamed properties: ", len(propSet))
    create_newPropFile(propSet)

    #newly added to collect all hindi property list 
    #All_en.sort()
    #AllProSet=set(All_en)
    AllProSet =  list(All_en_dict.keys())
    print("IN ENGLISH Number of TOTAL properties: ", len(All_en))
    print("IN ENGLISH Number of UNIQUE properties: ", len(AllProSet))
    create_newAllPropFile(AllProSet)

    print("Temp file generated for unnamed properties: "+"tmp_proplist.txt")
    #print(propSet)

if __name__ == "__main__":
    main()


