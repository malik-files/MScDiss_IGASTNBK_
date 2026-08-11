This is the readme for the document.

A description of the files and folders are seen below.

In folder, Main Code
- "requirements.txt" - this contains the python libraries and their versions used for the project.
- Visuals Data/ - This is a collection of the counts of various entities in the dataset and the results of group bys. 
It is meant to be used to create visualisations. Rerunning the code will update them to the most correct results. 
- missingValuesStore/ - contains entities in the datasets who have certain missing values. Refer to file name to disambiguate.
- mapData/ - This contains the free to use data obtained from naturalearthdata.com.
- Group Info/ - Is a collection of some csv files obtained from wikidata to do some of the group analysis.
It is included so fun of the code can be run.
- graphTesting/ - this is the code that was copied to the GPU cluster to perform link prediction.
- graphs/ - is a collection of some of the graph files created. Some of the code used to make some of the ego graphs may have been deprecated and removed.
- func/UsefulFunctions.py - these are the functions that are used throughout the program to reduce the amount of code duplication.
- Find_The_Music_Files/ -This file contains the code to extract the names of files in the genre English Wikipedia pages. 
  - getMusicalFiles.ipynb extracts only the audio files.
  - getAllFileTypes.ipynb collects all the embedded images, videos, and audio file names in the article.
- Data contains some of the data needed to run the analysis 
    Outside the MainCode