#!/usr/bin/env python
"this script imports mongo and the db and print the first document of the db"

import pymongo

CONNECTION = pymongo.Connection()

DB = CONNECTION["sviepbd"]

# RESULTS = DB.results
RESULTS_COMPLETE = DB.results_complete

print RESULTS_COMPLETE.find_one()['tokens_bag']

# Vectorizing tries...not working right now, i have to find the right library from sklearn

RESULTS_BAGS = RESULTS_COMPLETE.find(limit=1, fields=["tokens_bag"])

RESULTS_BAGS_LIST = []

for bag in RESULTS_BAGS:
    RESULTS_BAGS_LIST.append(bag["tokens_bag"])

print RESULTS_BAGS_LIST

from sklearn.feature_extraction import DictVectorizer

VEC = DictVectorizer()

VEC.fit_transform(RESULTS_BAGS).toarray()




