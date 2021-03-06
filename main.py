#!/usr/bin/env python
"this script imports mongo and the db and print the first document of the db"

import pymongo

# Imports useful packages
import numpy as np
import scipy.sparse as sparse

import SparsePCA as our_spca
import operator as op

from sklearn.decomposition import SparsePCA
from pprint import pprint

def import_csv_matrix(path, delimiter, is_word):
    "returns a matrix from a csv file like ours"
    # sparse_matrix = np.loadtxt(open(path, "rb"), delimiter=delimiter, dtype={'names':('i', 'j', 'val'), 'formats': ('int', 'int', 'float')})   
    if is_word: 
        dtype = np.dtype({'names': ['indice', 'word'], 'formats': ['i32', 'a30']})
        csv_matrix = np.loadtxt(open(path, "rb"), delimiter=delimiter, dtype=dtype)
    else:
        dtype = np.dtype({'names': ['indicedoc', 'indiceword', 'val'], 'formats': ['i32', 'i32', 'f8']})
        # dtype = np.dtype({'names': ['indicedoc', 'indiceword', 'val'], 'formats': ['i32', 'i32', 'f8']})
        csv_matrix = np.loadtxt(open(path, "rb"), delimiter=delimiter, dtype=dtype) 

    return csv_matrix

def csv_to_sparse(csv_matrix, n_lines, n_columns):
    "transforms a csv bag of words import into a sparse matrix"
    # 421 docs , 32614 words for few
    # 9000 docs, 2949 mots for many
    sparse_matrix = sparse.coo_matrix((np.array(csv_matrix['val']), (np.array(csv_matrix['indiceword']), np.array(csv_matrix['indicedoc']))), shape=(n_lines, n_columns))
    return sparse_matrix

def words_from_component(component_matrix, word_matrix):
    "return the components vectors as weigthed words"
    res = []
    non_zero_is = np.nonzero(component_matrix)[0].tolist()
    print non_zero_is
    for i in non_zero_is:
        res.append([word_matrix[i][1], component_matrix[i]])
    return sorted(res,key=op.itemgetter(1),reverse=True)

def insert_res_in_mongodb(res, params, n_components):
    "Insert the result of our spca in the db so it can be stored, retrieved and displayed in a web interface later"
    # Connects to Mongo DB and use the collection "components"
    connection = pymongo.Connection('127.0.0.1', 3001)
    database = connection["meteor"]
    components = database.comps

    """
    record structure
    {
    params, 
    n_components : 4,
    components : {
        1 : {
            1 : {word, weight}
            2 : {word, weight}
            ...
        }
        ...
    }}
    """

    same_record = components.find_one(params)

    record = params
    record['n_components'] = n_components
    record['components'] = {}

    n_component = 1
    for word_component in res:

        component_record = {}        
        n_word = 1
        for word in word_component:

            component_record[str(n_word)] = {
                'word':word[0],
                'weight':word[1]
            }

            n_word = n_word + 1

        record['components'][str(n_component)] = component_record
        n_component = n_component + 1

    if same_record == None:
        print "creating new record for this result..."
        components.insert(record)
        return

    if same_record['n_components'] < record['n_components']:
        print "updating existing record with new components..."
        components.update({"_id":same_record['_id']}, record)
        return
    else:
        print "no need to update, last result better"

def run_spca(matrix_path, n_lines, n_col, word_path, delimiter, k, h, n_components, norm_row, precision):
    "Run our algorithm with all the parameters"

    print "Beggining the spca with our algorithm..."
    csv_matrix = import_csv_matrix(matrix_path, delimiter, False)
    sparse_matrix = csv_to_sparse(csv_matrix, n_lines, n_col)
    components = our_spca.components(sparse_matrix, k, h, n_components, norm_row, precision)
    word_matrix = import_csv_matrix(word_path, delimiter, True)
    res = []
    for component in components:
        res.append(words_from_component(component, word_matrix))

    params = {
        'matrix_path':matrix_path,
        'n_lines':n_lines,
        'n_col':n_col,
        'word_path':word_path,
        'k':k,
        'h':h,
        'norm_row':norm_row,
        'precision':precision
    }

    insert_res_in_mongodb(res, params, n_components)

    return res

    # Examples
    # res = run_spca("../data/many-results_matrix.csv", 2950, 9000, "../data/many-results_words.csv", " ", 50, 2000, 6, False, 1.0e-8)
    # res = run_spca("../data/few-results_matrix.csv", 2950, 9000, "../data/few-results_words.csv", " ", 32615, 421, 6, False, 1.0e-8)
    # pprint(res) ## pretty-printing, more readable

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
    """Vectorizing tries...not working right now, but it is ok since Valentin provided this code already in the other repository"""

    results_bags = token_bags_cursor.find(limit=1, fields=["tokens_bag"])

    results_bags_list = []

    for bag in token_bags_cursor:
        results_bags_list.append(bag["tokens_bag"])

    print results_bags_list

    from sklearn.feature_extraction import DictVectorizer

    vec = DictVectorizer()

    vec.fit_transform(results_bags).toarray()

# do the SparsePCA with scikit learn
def do_sparse_pca(sparse_matrix):
    # from skikit learn http://scikit-learn.org/stable/modules/generated/sklearn.decomposition.SparsePCA.html#sklearn.decomposition.SparsePCA

    dense_matrix = sparse_matrix.tobsr().toarray()
    # instantiate the spca with some parameters
    spca = SparsePCA(n_components=6, alpha=0.01, ridge_alpha=0.01, max_iter=1000, tol=1e-08, method='lars', n_jobs=1, U_init=None, V_init=None, verbose=False, random_state=None)

    # train the spca with our matrix
    spca.fit(dense_matrix)

    # return the components
    return spca.components_

def main_scikit_many():
    print "Beginning the sparse pca with scikit for many results"
    # Providen you have the "data" repo next to this folder
    sparse_matrix = csv_to_sparse(import_csv_matrix("../data/many-results_matrix.csv", " ", False), 2950, 9000)

    word_matrix = import_csv_matrix("../data/many-results_words.csv", " ", True)

    component = do_sparse_pca(sparse_matrix)

    words_from_component(component[0], word_matrix)
