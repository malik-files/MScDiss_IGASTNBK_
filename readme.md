This is the readme for the document.

A description of the files and folders are seen below.

In folder, Main Code
- "requirements.txt" - this contains the python libraries and their versions used for the project.
- Visuals Data/ - This is a collection of the counts of various entities in the dataset and the results of group bys. 
It is meant to be used to create visualisations. Rerunning the code will update them to the most correct results. 
- missingValuesStore/ - contains entities in the datasets who have certain missing values. Refer to file name to disambiguate.
- mapData/ - This contains the free to use data (maps) obtained from naturalearthdata.com, and countries connected to their identifier obtained from Wikidata.
- Group Info/ - Is a collection of some csv files obtained from wikidata to do some of the group analysis.
It is included so fun of the code can be run.
- graphTesting/ - this is the code that was copied to the GPU cluster to perform link prediction.
- graphs/ - is a collection of some of the graph files created. Some of the code used to make some of the ego graphs may have been deprecated and removed.
- func/UsefulFunctions.py - these are the functions that are used throughout the program to reduce the amount of code duplication.
- Find_The_Music_Files/ -This file contains the code to extract the names of files in the genre English Wikipedia pages. 
  - getMusicalFiles.ipynb extracts only the audio files.
  - getAllFileTypes.ipynb collects all the embedded images, videos, and audio file names in the article.
- Data contains some of the data needed to run the analysis files
- label_artist_from_wikidata.ipynb and label_merging_groups_wikidata.ipynb - is the file used to label and merge the results from the sparql query.
These files, but the .csv files are available on request are not included
in the submission but their results which are used to run the other files are so code outside of the labelling and merging process is executable.
- statisticalTests.ipynb - includes the code used to perform the two proportion z-test.
- OMBD-ps.py - this is code used to create dataset of musicbrainz data using API requests. This code is deprecated now as the use of JSON dumps
was preferred. It is included for the sake of completeness.
- inspecting_analysing_wikidata_groups.ipynb, inspecting_analysing_group_MB_data.ipynb, inspecting_analysing_artist_MB_data.ipynb, cleaning_inspecting_labelling_Wikidata_artists.ipynb
  - The files above are used to analyse the created datasets/parquet files in Data/
- getGenreFromMB.py - obtains the music genres from musicBrainz using API calls.
- gettingArtistsFromMBJSON.py and gettingGroupsFromMBJSON.py - These are used to filter the MusicBrainz JSON dump and obtain smaller more useable files.
- gaps_wikidata_mb.py - compares the data from wikidata and MusicBrainz.
- create_knowledge_graph_* files: These are the files used to create the knowledge graphs/networks that would be visualised with Gephi

Outside the MainCode

- A selection of images of the graphs can be seen in Graph Images/.
- Results Collation - Wikidata Sparql.docx contains the sparql queries used to obtain the initial dataset from Wikidata