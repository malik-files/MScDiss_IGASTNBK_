#!/usr/bin/python3



import requests
import pandas as pd


def getAllFiles(title):

    """
    This code has been adapted from the example code from Mediawiki.
    Accessed on 2/07/2026 from https://www.mediawiki.org/wiki/API:Images

    Original Text below: 
    get_page_images.py

    MediaWiki API Demos
    Demo of `Images` module: Send a GET request to obtain a JSON
	object listing all of the image files embedded on a single page

    MIT License

"""


    S = requests.Session()
    URL = "https://en.wikipedia.org/w/api.php"
    headers = {'User-Agent': 'MAlikDiss/1.0 (aja25@st-andrews.ac.uk)'}

    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "images"
    }

    R = S.get(url=URL, params=PARAMS, headers=headers)
    DATA = R.json()

    PAGES = DATA['query']['pages']
    files = set()

    for k, v in PAGES.items():
        for img in v['images']:
            files.add(img["title"])

    return files

def getGenres(genreCSV):
    genreTable = pd.read_csv()
