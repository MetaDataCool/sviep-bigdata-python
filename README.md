sviep-bigdata-python
====================

Mongo Databases dumps :

To copy the entire pre-tokenized mongo db of 

 - "results" : 9000 results, some in French with approximate ranking; the target websites have not been scraped. Tokenized.
- "results2": 548 results, only in English and with exact ranking (not very useful).
- "results_complete": 421 results documents (those of the above which websites have been fetched successfully). Tokenized.

that is in /sviepdb_backup/sviepbd into your mongodb
be sure to have your instance of mongod up and running and a a database called scviepbd. Then:

mongorestore --db sviepbd path/to/sviepbd_backup/sviepbd

(you need to have a database called scviepbd to do that)

that will copy into your mongo instance the tokenized collections

tokenized means that each document has a "tokens_bag" key; it's an array of {"word": <word>, "weight": <number>}

Python Setup

you need to have python, an environment where you can run it, the packages pymongo and sklearn.

I am using personally Sublime Text 3, with the SublimeREPL plugin, installed with Package control.

Python program

main.py can be run and right now does

 Take the csv file and import it in python
 http://stackoverflow.com/questions/4315506/load-csv-into-2d-matrix-with-numpy-for-plotting




has legacy script to do
 - imports pymongo package to connect to the mongodb from python
 - print the first bag of words 

 - (then uses http://scikit-learn.org/stable/modules/feature_extraction.html to create the (i,j) val() matrix)

 Take the csv and import it in python
 http://stackoverflow.com/questions/4315506/load-csv-into-2d-matrix-with-numpy-for-plotting

