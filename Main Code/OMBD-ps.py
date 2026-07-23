#Need to query for all the artists on musicbrainz
#Maybe search by type

import musicbrainzngs
import pandas as pd


#Do a loop to search and then merge the pandas data frames into it then drop unnecessary fields after

musicbrainzngs.set_useragent("MalikDiss","1.0",contact="aja25@st-andrews.ac.uk")

groupType = ["Person", 'Group', 'Orchestra','Choir', 'Other']
for group in groupType:
    offset = 0
    artistCount = 0
    listOfApiResults = []
    listOfApiResults2 = list()

    while offset <= artistCount:
        searchResults = musicbrainzngs.search_artists(limit='100',offset=offset,strict=True,type=group)
        if offset == 0:
            print(searchResults["artist-count"], " is the artist count")
            print(searchResults)
            artistCount = searchResults["artist-count"]
            
            listOfApiResults = list(searchResults["artist-list"])
            #print(len(listOfApiResults))
        else:
            listOfApiResults2 = list(searchResults["artist-list"])
            #print(listOfApiResults2)
            #print(searchResults)
            #concatenate the two dataframes
            print(f"the size of list 2 is {len(listOfApiResults2)}")
            #Was running into issues with list append so used list extend instead to properly join the lists
            listOfApiResults.extend(listOfApiResults2)
            print(f"The size of the list now is {len(listOfApiResults)}")
        offset = offset + 100
        print(f"offset amount:{offset}")
        if len(listOfApiResults) == artistCount:
            break

    df = pd.json_normalize(listOfApiResults)
    df.to_csv(f"{group}-musicBrainzData.csv", index=False)
            

print(len(listOfApiResults))