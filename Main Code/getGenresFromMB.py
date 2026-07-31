# %%
import requests
import pandas as pd
import numpy as np
# %%
def getGenresFromMusicBrainz():

    genres_musicBrainz = dict()
    genre_count = 0
    offset = 0
    S = requests.Session()
    URL = "https://musicbrainz.org/ws/2/genre/all?"
    headers = {'User-Agent': 'MAlikDiss/1.0 (aja25@st-andrews.ac.uk)'}

    while len(genres_musicBrainz.keys()) <= genre_count:
        
        #This was created with the aid of Mediawiki's API sandbox tool accessiible here: https://www.wikidata.org/wiki/Special:ApiSandbox#action=wbgetentities&format=json&ids=Q180736&props=labels&languages=en&languagefallback=1&sitefilter=&formatversion=2
        PARAMS = {
            "fmt": "json",
            "limit": 100,
            "offset":offset
        }

        #added the try-except for the scenarios as there were recurring issues with the api and i wanted to keep trying until
    
        try:
            
            R = S.get(url=URL, params=PARAMS, headers=headers)
            DATA = R.json()
            genre_count = DATA['genre-count']
            print(f"The genre count is {genre_count}")
            RETURNVALUE = DATA['genres']
            print(RETURNVALUE)
            for item in RETURNVALUE:
                genres_musicBrainz[item['id']] = item['name']
            offset = offset + 100
            
        except Exception as e:
            print(f"Ran into an issue with the API: {e}")
            
        
        if len(genres_musicBrainz.keys()) == genre_count:
            break

   
    return genres_musicBrainz

genresDict = getGenresFromMusicBrainz()
print(len(genresDict.keys()))

#Turn the genre dictionary to a csv file so i can save items
#Over 2165 genres on the day I created this
# with open("genre-musicBrainzID.csv","+w") as file:
#     file.write("genre,musicBrainzID\n")
#     for k,v in genresDict.items():
#         file.write(f"{k},{v}\n")
# print("Created the file")
print(f"The number of genres in the dictionary is {len(genresDict.keys())}")
genresDF = pd.DataFrame(genresDict.items(), columns=["musicBrainzID", "genre"])
genresDF.to_csv("./Data/musicBrainz_Genres.csv",index=False)
