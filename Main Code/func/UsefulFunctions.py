#This function is used to get the entity numbers
import requests 
import datetime as dt

def getEntityIDValue(link):
    try:
        value = link.split("/")[-1]
        return value.strip()
    except:
        return link

#This makes the genre dictionaries into a list of genres

def prettifyGenres(item):
    genreList = []
    for x in item:
        genreList.append(x.get("name",None))
    return genreList

def getLabelWithSparql(listOfIDS):

    #This code was adapted from a Stack Overflow question "How to integrate Wikidata query in python" by emj. 
    #Accessed on 5 July 2026 from https://stackoverflow.com/a/64899794
    #This code makes use of the values clause that is discussed in the Wikidata Sparql tutorial
    #Accessed 5/07/2026 accessible: https://www.wikidata.org/wiki/Wikidata:SPARQL_tutorial 
    dictionaryOfLabels = dict()
    while len(dictionaryOfLabels.keys()) == 0:
        print(f"This is the list of ids: {listOfIDS}")
        url = 'https://query.wikidata.org/sparql'
        headers = {'User-Agent': 'MAlikDiss/1.0 (aja25@st-andrews.ac.uk)'}
    
        query =  '''
                    SELECT ?item ?itemLabel
                    WHERE {
                        VALUES ?item ''' + listOfIDS + '''

                    SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],mul,en" . }
                    }
        '''
        try:
            r = requests.get(url, params = {'format': 'json', 'query': query}, headers=headers)
            data = r.json()
            results = data['results']['bindings']
            print(results)
            for item in results:
                dictionaryOfLabels[getEntityIDValue(item['item']['value'])] = item['itemLabel']['value']
            
            
        except Exception as e:
            print(f"There was an error: {e}")
    print(dictionaryOfLabels.values())
    
    return dictionaryOfLabels

def processEntityNumbers(listOfEntityNumbers):
    stringForQuerying = str()
    for x in listOfEntityNumbers:
        stringForQuerying = stringForQuerying + " wd:" + str(x)
    
    #get rid of any lingering white space
    stringForQuerying = stringForQuerying.strip()
    stringForQuerying = "{" + stringForQuerying + "}"
    return stringForQuerying

def getLabels(listOfIDS):
    dictionaryOfLabels = dict()
    if len(listOfIDS) > 0:
        dictionaryOfLabels = {k : None for k in listOfIDS}
    else:
        raise Exception("No IDS provided")
    return addEntityLabels(dictionaryOfLabels)

    return
def addEntityLabels(dictionary):
    #Do it in groups of 500
    keys = list(dictionary.keys())
    print(f"The number of keys in the dictionary is {len(keys)} ")
    x = 0
    while x < len(dictionary.keys()):
        keysForSearch = keys[x:min(x+400, len(dictionary.keys()) + 1)]
        #print(f"The keysForSearch is {keysForSearch}")
        queryString = processEntityNumbers(keysForSearch)
        updatedDict = getLabelWithSparql(queryString)
        #print(updatedDict)
        dictionary.update(updatedDict)
        x += 400
    
    return dictionary

#Tested wit the date: "1989-01-01T00:00:00Z" and it successfully returned 1989
'''
This function takes in a string (which is time) and extarcts the year out of it to return a integer
'''
def getYear(time: str) -> int | None:
    try:
        date_time = dt.datetime.strptime(time, "%Y-%m-%dT%H:%M:%SZ")
        date_time = date_time.strftime('%Y')
        return(int(date_time))
    except:
        #This is for the situations where there is no start and end of work period so it doesn't return 
        #an error
        return None