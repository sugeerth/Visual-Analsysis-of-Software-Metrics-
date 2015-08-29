"""
Script that parses the data 
"""

import csv 
import numpy as np 

filename = 'data/camel_git_log.csv'

with open(filename, 'rb') as csvfile:
   reader = csv.reader(csvfile, delimiter=',', quotechar='\'')
   header = reader.next()
   VizData = np.array([line for line in reader])

""" Dictionaries for 2 and 3  """
FileId = dict()
# print VizData[3][3]
# print (VizData[2][])

# for i in range(len(VizData)):
# 	print VizData[i][2]

for i in range(47382):
	FileId[int(VizData[i][2])] = VizData[i][3]

FileNewId = dict()
for i in range(47382):
	FileNewId[int(VizData[i][2])] =  VizData[i][1],VizData[i][0]





import pprint
pprint.pprint(FileNewId)