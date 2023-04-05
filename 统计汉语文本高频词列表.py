#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 14:56:42 2022

@author: Merlin
"""

import os
import xlsxwriter

# Read the Chinese stop words from a file
with open('/Users/Merlin/Desktop/mylab/chinese_sfp.txt', 'r') as f:
    stop_words = set(f.read().splitlines())

# Create a dictionary to store the word frequency
word_freq = {}

# Loop through all the files in the corpus_files folder
for filename in os.listdir('/Users/Merlin/Desktop/mylab/wo_wu'):
    # Open the file and read its contents
    with open(os.path.join('/Users/Merlin/Desktop/mylab/wo_wu', filename), 'r') as f:
        text = f.read()
    
    # Split the text into words
    words = text.split()
    
    # Loop through the words and update the word frequency dictionary
    for word in words:
        # Ignore words in the stop word list
        if word not in stop_words:
            word_freq[word] = word_freq.get(word, 0) + 1

# Create an Excel file to store the results
workbook = xlsxwriter.Workbook('/Users/Merlin/Desktop/mylab/result_sfp.xlsx')
worksheet = workbook.add_worksheet()

# Write the words and their frequencies to the Excel file
row = 0
col = 0
for word, freq in sorted(word_freq.items(), key=lambda item: item[1], reverse=True):
    worksheet.write(row, col, word)
    worksheet.write(row, col + 1, freq)
    row += 1

# Save the Excel file
workbook.close()
