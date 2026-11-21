#-------------------------------------------------------------------------
# AUTHOR: Ryan Vu
# FILENAME: vsm_search.py
# SPECIFICATION: Builds a Vector Space Model search engine using TF-IDF 
#                (stopwords removed) and cosine similarity, then evaluates 
#                it against 5 queries by computing the Average Precision 
#                per query and Mean Average Precision.
# FOR: CS 4250 - Assignment 4
# TIME SPENT: 50 min
#-----------------------------------------------------------*/

# importing required libraries
from operator import itemgetter

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------
# 1. Load the input files
# ---------------------------------------------------------
docs = pd.read_csv("docs.csv")
queries = pd.read_csv("queries.csv")
judgments = pd.read_csv("relevance_judgments.csv")


# ---------------------------------------------------------
# 2. Build the TF-IDF matrix for the documents
# ---------------------------------------------------------
# Requirement: remove stopwords only
vectorizer = TfidfVectorizer(stop_words="english")
doc_matrix = vectorizer.fit_transform(docs["text"])


# ---------------------------------------------------------
# 3. Process each query and compute AP values
# ---------------------------------------------------------
ap_scores = {}
for _, row in queries.iterrows():
    qid = row["query_id"]
    query_vector = vectorizer.transform([row["query_text"]])
    scores = cosine_similarity(query_vector, doc_matrix)[0]
    ranked = docs.assign(score=scores).sort_values("score", ascending=False, kind="stable")["doc_id"]

    relevant = set(judgments[(judgments["query_id"] == qid) & (judgments["judgment"] == "R")]["doc_id"])


    # -----------------------------------------------------
    # 4. Compute Average Precision (AP)
    # -----------------------------------------------------

    # store the AP value for this query (use any data structure you prefer)
    hits = 0
    precision_sum =0
    for i in range(len(ranked)):
        if ranked.iloc[i] in relevant:
            hits += 1
            precision_sum += hits / (i + 1)

    ap_scores[qid] = precision_sum / len(relevant)

    




# ---------------------------------------------------------
# 5. Sort queries by AP in descending order
# ---------------------------------------------------------
sorted_queries = sorted(ap_scores.items(), key=itemgetter(1), reverse=True)


# ---------------------------------------------------------
# 6. Print the sorted queries and their AP scores
# ---------------------------------------------------------
print("====================================================")
print("Queries sorted by Average Precision (AP):")

for qid, ap in sorted_queries:
    print(f"{qid}: {ap:.4f}")

print("====================================================")
print(f"Mean Average Precision (MAP): {sum(ap_scores.values()) / len(ap_scores):.4f}")