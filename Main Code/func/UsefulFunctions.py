#This function is used to get the entity numbers
import requests 
import datetime as dt
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import squarify
import polars as pl

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


"""

Function to create new networkX graphsfrom a pandas dataframe 


"""
def addToNetwork4(df, source, target, connectionType, attr, attr2, sourceName, targetName):
    df["Type"] = connectionType
    newDF = df[[source, target, "Type"]]
    newDFGraphReady = newDF.dropna().drop_duplicates()
    graph = nx.from_pandas_edgelist(newDFGraphReady, source= source, target = target, edge_attr="Type", create_using=nx.DiGraph())

    #Add the other nodes
    graph.add_nodes_from(set(newDF[source].dropna().to_list()))
    graph.add_nodes_from(set(newDF[target].dropna().to_list()))


    #add attributes
    attributes = {k: {"EntityType": attr} for k in set(newDF[source].dropna().to_list())}
    attributes2 = {k: {"EntityType": attr2} for k in set(newDF[target].dropna().to_list())}

    #Add the name attributes

    sourceTuples = df[[source,sourceName]].apply(tuple, axis=1).to_list()
    targetTuples = df[[target,targetName]].apply(tuple, axis=1).to_list()

    attributesName1 = {k: {"Label" : v} for k,v in sourceTuples}
    attributesName2 = {k: {"Label": v} for k,v in targetTuples}



    nx.set_node_attributes(graph, attributes)
    nx.set_node_attributes(graph, attributes2)
    nx.set_node_attributes(graph, attributesName1)
    nx.set_node_attributes(graph, attributesName2)

    return graph

def makeBarChart(names, counts, title, yLabel):

    fig, ax = plt.subplots()
    labels = names
    counts = counts
    #bar_labels = ['red', 'blue', '_red', 'orange']
    bar_colors = ['tab:blue', 'tab:red', 'tab:orange']

    ax.bar(labels, counts, color=bar_colors)

    ax.set_ylabel(yLabel)
    ax.set_title(title)
    for container in ax.containers:
        ax.bar_label(container, fmt='{:,.0f}')
    #ax.legend(title='Fruit color')

    plt.show()

def horizontalBarChart(names, counts, title, yLabel):
    fig, ax = plt.subplots()
    y_pos = np.arange(len(names))
    hbars = ax.barh(y_pos, counts, align='center')

    ax.set_yticks(y_pos, labels=names)
    ax.invert_yaxis()
    ax.set_xlabel(yLabel)
    ax.set_title(title)

    plt.show()

def makePieChart2(labels, sizes, title, explode):
    labels = labels
    sizes = sizes


    fig, ax = plt.subplots()
    ax.set_title(title)
    ax.pie(sizes, labels=labels,  autopct='%1.1f%%', explode=explode)

def makePieChart(labels, sizes, title, colourPalette):
    labels = labels
    sizes = sizes
    colour = sns.color_palette(colourPalette, len(sizes))


    fig, ax = plt.subplots()
    #ax.set_title(title)
    ax.pie(sizes, labels=labels,  autopct='%1.1f%%', colors=colour)

def makeTreeMap(labels, counts, colourPalette, title,pad):
    colour = sns.color_palette(colourPalette, len(counts))
    ax = squarify.plot(counts, color=colour, pad = pad, norm_x= 300, norm_y=300)
    ax.get_xaxis().set_visible(False)
    plt.legend(handles=ax.containers[0], labels = labels, loc='center left')
    plt.title(title)

def groupBarChart(labels, counts1, counts2, title, yLabel, legend1, legend2):
    species = labels
    colour = sns.color_palette("coolwarm", 2)
    counts = {
        legend1: counts1,
        legend2: counts2,
    }

    fig, ax = plt.subplots(layout='constrained')

    res = ax.grouped_bar(counts, tick_labels=species, group_spacing=1, colors= colour)
    for container in res.bar_containers:
        ax.bar_label(container, fmt='{:,.0f}', padding=3)

    # Add some text for labels, title, etc.
    ax.set_ylabel(yLabel)
    ax.set_title(title)
    ax.legend(loc='best')

    plt.show()

def makeTop10(df, entity, column, columnLabel, site, title):

    print(f"There are {len(df[column].drop_nulls().unique())} {column}s for {entity}s on {site}.")

    groupedBY = df.group_by([column, columnLabel]).agg(pl.col(entity).count()).sort(by=pl.col(entity), descending=True)
    groupedByFRAC = df[column].drop_nulls().value_counts(sort=True, normalize=True, name="fraction")
    print(groupedByFRAC)
    groupedBY.write_csv(f"./Visuals Data/{site}{entity}GroupedBy{str(column).capitalize()}.csv", null_value="null/unknown")
    print(groupedBY.head(5))

    top10 = groupedBY.drop_nulls()[0:10]
    horizontalBarChart(top10[columnLabel].to_list(), top10[entity].to_list(), title, "Number of Groups" )