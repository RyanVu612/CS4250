#-------------------------------------------------------------------------
# AUTHOR: Ryan Vu
# FILENAME: inverted_index.py
# SPECIFICATION: Builds and maintains a MongoDB inverted index as documents are inserted, updated, and deleted
# FOR: CS 4250 - Assignment #3
# TIME SPENT: About 2-3 hours
#-------------------------------------------------------------------------

# Importing Python libraries
from pymongo import MongoClient

import string
from collections import Counter

# Connecting to MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Accessing the database and collections
db = client["assignment3"]
documents = db["documents"]
inverted_index = db["inverted_index"]
documents.delete_many({})
inverted_index.delete_many({})

#-------------------------------------------------------------------------
# FUNCTION: getTermFrequencies
# SPECIFICATION: receives a text and returns the frequency of each term
#-------------------------------------------------------------------------

def getTermFrequencies(text):
    # Converting text to lowercase
    text = text.lower()

    # Removing punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    
    # Splitting the text into terms
    terms = text.split()
    
    # Returning the term frequencies
    return Counter(terms)

#-------------------------------------------------------------------------
# FUNCTION: addPosting
# SPECIFICATION: adds a posting to an existing term or creates a new term
#-------------------------------------------------------------------------
def addPosting(term, docId, tf):
    # Searching for the term in the inverted index
    entry = inverted_index.find_one({"term": term})
    
    # Creating a new term if it does not exist
    if entry is None:
        inverted_index.insert_one(
            {"term": term, "postings": [{"docId": docId, "tf": tf}]}
        )
    # Adding a posting if the term already exists
    else:
        inverted_index.update_one(
            {"term": term},
            {"$push": {"postings": {"docId": docId, "tf": tf}}}
        )

#-------------------------------------------------------------------------
# FUNCTION: removePosting
# SPECIFICATION: removes a document posting from a term and deletes the
# term if its postings list becomes empty
#-------------------------------------------------------------------------
def removePosting(term, docId):
    # Removing the posting from the term
    inverted_index.update_one(
        {"term": term},
        {"$pull": {"postings": {"docId": docId}}}
    )
    
    # Retrieving the term after removing the posting
    entry = inverted_index.find_one({"term": term})
    
    # Deleting the term if its postings list is empty
    if entry is not None and len(entry["postings"]) == 0:
        inverted_index.delete_one({"term": term})

#-------------------------------------------------------------------------
# FUNCTION: insertDocument
# SPECIFICATION: inserts a document and updates the inverted index
#-------------------------------------------------------------------------
def insertDocument(document):
    # Inserting the document into the documents collection
    documents.insert_one(document)
    
    # Obtaining the term frequencies
    tfs = getTermFrequencies(document["text"])
    
    # Updating the inverted index
    for term, tf in tfs.items():
        addPosting(term, document["_id"], tf)

#-------------------------------------------------------------------------
# FUNCTION: updateDocument
# SPECIFICATION: updates a document and makes the corresponding changes
# to the inverted index
#-------------------------------------------------------------------------
def updateDocument(docId, newText):
    # Retrieving the current document
    doc = documents.find_one({"_id": docId})
    
    # Obtaining the old and new term frequencies
    oldTfs = getTermFrequencies(doc["text"])
    newTfs = getTermFrequencies(newText)
    
    # Processing terms that existed in the old document
    for term, oldTf in oldTfs.items():
        if term not in newTfs:
            removePosting(term, docId)
        elif newTfs[term] != oldTf:
            removePosting(term, docId)
            addPosting(term, docId, newTfs[term])
    
    # Processing terms that occur only in the new document
    for term, tf in newTfs.items():
        if term not in oldTfs:
            addPosting(term, docId, tf)
    
    # Updating the document text
    documents.update_one(
        {"_id": docId},
        {"$set": {"text": newText}}
    )

#-------------------------------------------------------------------------
# FUNCTION: deleteDocument
# SPECIFICATION: deletes a document and removes all of its postings from
# the inverted index
#-------------------------------------------------------------------------
def deleteDocument(docId):
    # Retrieving the document before deleting it
    doc = documents.find_one({"_id": docId})
    
    # Obtaining the terms contained in the document
    tfs = getTermFrequencies(doc["text"])
    
    # Removing the document from every corresponding posting list
    for term in tfs:
        removePosting(term, docId)
    
    # Deleting the document
    documents.delete_one({"_id": docId})

#-------------------------------------------------------------------------
# Executing the sequence of operations
#-------------------------------------------------------------------------
# Operation 1: document 1 is obtained
document1 = {
    "_id": 1,
    "text": "Summer rain is common in Florida."
}

insertDocument(document1)

# Operation 2: document 2 is obtained
document2 = {
    "_id": 2,
    "text": "Summer is hot in Arizona."
}

insertDocument(document2)

# Operation 3: document 1 is updated
updateDocument(
    1,
    "Summer rain is hot rain in Florida."
)

# Operation 4: document 3 is obtained
document3 = {
    "_id": 3,
    "text": "Hot summer rain in California."
}

insertDocument(document3)

# Operation 5: document 1 is deleted
deleteDocument(1)

# Operation 6: print the content of the documents and inverted_index collections
print("documents:")

for doc in documents.find().sort("_id"):
    print(doc)

entries = inverted_index.find(
    {},
    {"_id": 0}
).sort("term")

print("\ninverted_index:")
for entry in entries:
    print(entry)


