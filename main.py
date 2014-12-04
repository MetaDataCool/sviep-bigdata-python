#!/usr/bin/env python
"this script imports mongo and the db and print the first document of the db"

import pymongo

# Imports useful packages 
import numpy as np

# Returns a matrix from the csv file
def import_csv_matrix(path, delimiter):
    # the weird comment below is just to disable my text/error highlighter plugin for one line "./matrices_creuses/few-results_matrix.csv"
    # pylint: disable=E1103
    sparse_matrix = np.loadtxt(open(path, "rb"), delimiter=delimiter)
    # pylint: enable=E1103 
    return sparse_matrix  

def main():
    print "Launch approval"
    import_csv_matrix("./matrices_creuses/few-results_matrix.csv", " ") 

main()

# ================= Old Code
# Connects to Mongo DB and returns the pointer for the collection
def retrieve_bags_from_collection(limit):
    # Connects to Mongo DB
    connection = pymongo.Connection()
    database = connection["sviepbd"]
    # RESULTS = DB.results
    results_complete = database.results_complete
    # Returns a collection projected
    return results_complete.find(limit=limit, fields=["tokens_bag"])


def vectorize_bags(token_bags_cursor):
    # Vectorizing tries...not working right now, but it is ok since Valentin provided this code already in the other repository

    results_bags = token_bags_cursor.find(limit=1, fields=["tokens_bag"])

    results_bags_list = []

    for bag in token_bags_cursor:
        results_bags_list.append(bag["tokens_bag"])

    print results_bags_list

    from sklearn.feature_extraction import DictVectorizer

    vec = DictVectorizer()

    vec.fit_transform(results_bags).toarray()


# pylint: disable=E1103
SPARSE_MATRIX = np.loadtxt(open("./matrices_creuses/few-results_matrix.csv", "rb"), delimiter=" ")
# pylint: enable=E1103
