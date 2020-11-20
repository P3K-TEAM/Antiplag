# README:
# This script will analyse .txt files in the given folder

import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import json

# Write names of files to be checked for plagiarism # TODO: Files the user uploaded
testing = ['tested.txt', 'file 1.txt']
# Open corpus to be checked for plagiarism - NOTE: Has to contain also testing files #TODO: Our scrapped corpus
database = [doc for doc in os.listdir() if doc.endswith('.txt')]
# Just reading the files
database_text = [open(File).read() for File in  database]

# Vectorization of words and plag similarity
vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])

# Creating vectors and assigning them to the files
database_vectors = vectorize(database_text)
s_vectors = list(zip(database, database_vectors))



def plagiarism():
    global s_vectors
    for file_tested, vector_tested in s_vectors:
        # Only test files will go into testing
        if file_tested not in testing:
            continue
        for file_corpus, vector_corpus in s_vectors:
            # Do not compare against yourself
            if file_tested == file_corpus:
                continue
            score = similarity(vector_tested, vector_corpus)[0][1]
            result = (file_tested, file_corpus, score)
            plagiarism_results.add(result)

plagiarism_results = set()
plagiarism()


# Json creating
result_id = 5  # Add an incrementing hashing of result IDs
threshold = 0.15 # Threshold limit when a plagiarism is counted as a match, e.g. at least 15% must be matching

docs = []
for file in testing:
    matches = []
    for tested, corpus, score in plagiarism_results:
        if tested == file and score > threshold:
            matches.append({
            "name": corpus,
            "percentage": score,
            "matches": [ # Staticka hodnota zatial kedze vectorizacia mi nevrati presne kde to je plagiat
                {
                    "char_from": 15,
                    "char_to": 19
                }
            ]
            })

    docs.append({
        "id": testing.index(file),  # make IDs of documents by some hash function?
        "name": file,
        "percentage": 0.15, # Staticka hodnota zatial, bude treba vytvorit funkciu na coverage plagiatu textu
        "text": open(file).read(),
        "matches_docs": matches
    })

result_json = {
    "id_result": result_id,
    "documents": docs,
}

# Saving results as "result_ID.json" files
with open('result_' + str(result_id) + '.json' , 'w') as json_file:
    json.dump(result_json, json_file)
