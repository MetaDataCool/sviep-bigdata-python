#!/usr/bin/env python
"this script imports mongo and the db and print the first document of the db"

import pymongo

# Imports useful packages
import numpy as np
import scipy.sparse as sparse

import SparsePCA as our_spca

from sklearn.decomposition import SparsePCA

# Returns a matrix from the csv file
def import_csv_matrix(path, delimiter, is_word):
    # the weird comment below is just to disable my text/error highlighter plugin for one line "./matrices_creuses/few-results_matrix.csv"
    # pylint: disable=E1103
    # sparse_matrix = np.loadtxt(open(path, "rb"), delimiter=delimiter, dtype={'names':('i', 'j', 'val'), 'formats': ('int', 'int', 'float')})   
    if is_word: 
        dtype = np.dtype({'names': ['indice', 'word'], 'formats': ['i32', 'a30']})
        csv_matrix = np.loadtxt(open(path, "rb"), delimiter=delimiter, dtype=dtype)
    else:
        dtype = np.dtype({'names': ['indicedoc', 'indiceword', 'val'], 'formats': ['i32', 'i32', 'f8']})
        # dtype = np.dtype({'names': ['indicedoc', 'indiceword', 'val'], 'formats': ['i32', 'i32', 'f8']})
        csv_matrix = np.loadtxt(open(path, "rb"), delimiter=delimiter, dtype=dtype) 
    # pylint: enable=E1103 
    return csv_matrix

# transforms a csv bag of words import to a sparse matrix
def csv_to_sparse(csv_matrix, n_lines, n_columns):
    # 421 docs , 32614 words for few
    # 9000 docs, 2949 mots for many
    sparse_matrix = sparse.coo_matrix((np.array(csv_matrix['val']), (np.array(csv_matrix['indiceword']), np.array(csv_matrix['indicedoc']))), shape=(n_lines, n_columns))
    return sparse_matrix

def words_from_component(component_matrix, word_matrix):
    non_zero_is = np.nonzero(component_matrix)[0].tolist()
    print non_zero_is
    for i in non_zero_is:
        print component_matrix[i], word_matrix[i]

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

def main_scikit():
    print "Beginning the sparse pca with scikit"
    # Providen you have the "data" repo next to this folder
    return do_sparse_pca(csv_to_sparse(import_csv_matrix("../data/few-results_matrix.csv", " ", False), ))

def main_our_spca_few():
    print "Beginning the sparse pca with our powit implementation"
    # 421 docs (j) , 32615 words (i) for few
    # 9000 docs, 2949 mots for many
    sparse_matrix = csv_to_sparse(import_csv_matrix("../data/few-results_matrix.csv", " ", False), 32615, 421)
    component = our_spca.powit(sparse_matrix, 50, 500)[0]
    word_matrix = import_csv_matrix("../data/few-results_words.csv", " ", True)
    words_from_component(component, word_matrix)

def main_our_spca_many():
    print "Beginning the sparse pca with our powit implementation for many results"
    # 421 docs (j) , 32615 words (i) for few
    # 9000 docs, 2950 mots for many
    sparse_matrix = csv_to_sparse(import_csv_matrix("../data/many-results_matrix.csv", " ", False), 2950, 9000)
    component = our_spca.powit(sparse_matrix, 50, 2000)[0]
    word_matrix = import_csv_matrix("../data/many-results_words.csv", " ", True)
    words_from_component(component, word_matrix)



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
