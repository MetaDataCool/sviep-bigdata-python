#!/usr/bin/env python
"this script imports mongo and the db and print the first document of the db"

import pymongo

# Imports useful packages
import numpy as np
import scipy.sparse as sparse

from sklearn.decomposition import SparsePCA

# Returns a matrix from the csv file
def import_csv_matrix(path, delimiter):
    # the weird comment below is just to disable my text/error highlighter plugin for one line "./matrices_creuses/few-results_matrix.csv"
    # pylint: disable=E1103
    # sparse_matrix = np.loadtxt(open(path, "rb"), delimiter=delimiter, dtype={'names':('i', 'j', 'val'), 'formats': ('int', 'int', 'float')})    
    csv_matrix = np.loadtxt(open(path, "rb"), delimiter=delimiter)
    # pylint: enable=E1103 
    return csv_matrix

# transforms a csv bag of words import to a sparse matrix
def csv_to_sparse(csv_matrix):
    sparse_matrix = sparse.coo_matrix(csv_matrix[:, 2], (csv_matrix[:, 0], csv_matrix[:, 1]))
    return sparse_matrix

# do the SparsePCA
def do_sparse_pca(sparse_matrix):
    # from skikit learn http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.SparsePCA.html#sklearn.decomposition.SparsePCA

    dense_matrix = sparse_matrix.tobsr().toarray()
    # instantiate the spca with some parameters
    spca = SparsePCA(n_components=1, alpha=1, ridge_alpha=0.01, max_iter=1000, tol=1e-08, method='lars', n_jobs=1, U_init=None, V_init=None, verbose=False, random_state=None)

    # train the spca with our matrix
    spca.fit(dense_matrix)

    # return the components
    return spca.components_

def main():
    print "Launch approval"
    # Providen you have the "data" repo next to this folder
    print do_sparse_pca(csv_to_sparse(import_csv_matrix("../data/few-results_matrix.csv", " ")))

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
