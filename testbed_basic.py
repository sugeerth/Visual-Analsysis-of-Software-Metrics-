import csv
import sys
import datetime

#filen = sys.argv[1]
#metric = sys.argv[2]

filen = 'data/camel_git_log_data_wmetrics_modified_timestamp_fileindex.csv'
metric = 'countlinecode'

file_blocks = {}

csv_rows = []
with open(filen, 'rb') as csvfile:
	csv_file = csv.DictReader(csvfile, delimiter=',')
	for row in csv_file:
		csv_rows.append(row)


# Iterate through csv_rows to get y coords and x coords
for row in csv_rows:
	x_coord = row['committer_dt']
	metric_value = row[metric]
	#print (x_coord, metric_value, row['file_name_id'])
	if row['file_name_id'] in file_blocks.keys():
		file_blocks[row['file_name_id']].append((x_coord, metric_value))
	else:
		file_blocks[row['file_name_id']] = [(x_coord, metric_value)]



