
#-------------------------------------------------------------------------
# AUTHOR: Ryan Vu
# FILENAME: index.py
# SPECIFICATION: Inverted index of collection.csv
# FOR: CS 4250 - Assignment #1
# TIME SPENT: 30 minutes
#-------------------------------------------------------------------------

# Importing Python libraries
from collections import defaultdict
import pandas as pd

# Reading the document collection
data = pd.read_csv("collection.csv")

# Defining the dictionary used for lemmatization
# --> add your Python code here
lemmas = {}
lemmas["homes"] = "home"
lemmas["increases"] = "increase"
lemmas["increasing"] = "increase"
lemmas["rising"] = "rise"
lemmas["sales"] = "sale"

# Creating the data structure that will store the inverted index
# Use set in case of duplicate value in same query
invertedIndex = defaultdict(list)
invertedIndexSet = defaultdict(set)

# Processing each document in the collection
for i, row in data.iterrows():

    docID = row["Document"]
    text = row["Text"]

    # Applying surface-level normalization
    text = text.lower()
    text = text.translate(str.maketrans("", "", ".!?"))

    # Tokenizing the document
    words = text.split(' ')

    # Applying lemmatization
    # --> add your Python code here
    for i in range(len(words)):
        if words[i] in lemmas:
            words[i] = lemmas[words[i]]

    # Building the inverted index
    # --> add your Python code here
    for word in words:
        if docID not in invertedIndexSet[word]:
            invertedIndexSet[word].add(docID)
            invertedIndex[word].append(docID)

# Printing the inverted index with terms ordered alphabetically
# Expected format:
# term1 : ['Doc1', 'Doc2']
# term2 : ['Doc3']
# --> add your Python code here

# Alphabetize
invertedIndex = dict(sorted(invertedIndex.items()))

# Print inverted index
for key, value in invertedIndex.items():
    print(f"{key}\t: {value}")
