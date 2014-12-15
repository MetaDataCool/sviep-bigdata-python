#!/usr/bin/env python
"""
this script has be to called with parameters in the command line 
from meteor in order to run our algorithm
"""

from main import run_spca

from sys import argv

script, matrix_path, n_lines, n_col, word_path, k, h, n_components, norm_row, precision = argv

# run_spca("/Users/mcoenca/Documents/Thnktwice/Code/data/many-results_matrix.csv", 2950, 9000, "/Users/mcoenca/Documents/Thnktwice/Code/data/many-results_words.csv", " ", 10, 8000, 3, False, 1.5e-7)

run_spca(matrix_path, int(n_lines), int(n_col), word_path, " ", int(k), int(h), int(n_components), norm_row == "True", float(precision))
