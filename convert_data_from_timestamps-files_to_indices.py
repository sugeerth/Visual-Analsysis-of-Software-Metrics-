import csv
import sys
import datetime

filen = sys.argv[1]

dates = []
file_name_ids = []
with open(filen, 'rb') as csvfile:
	csv_file = csv.DictReader(csvfile, delimiter=',')
	for row in csv_file:
		dates.append(datetime.datetime.strptime(row['committer_dt'], '%Y-%m-%d %H:%M:%S'))
		file_name_ids.append(int(row['file_name_id']))
min_date = min(dates)
max_date = max(dates)
total_delta_seconds = (max_date - min_date).total_seconds()
file_name_ids = list(set(file_name_ids))
file_name_ids.sort()

with open(filen, 'rb') as csvfile:
	with open(filen[:-4] + '_modified_timestamp_fileindex.csv', 'wb') as outf:
		csv_file = csv.DictReader(csvfile, delimiter=',')
		fieldnames = csv_file.fieldnames
		fieldnames.append('file_name_index')
		csv_outf = csv.DictWriter(outf, fieldnames = csv_file.fieldnames, delimiter=',')
		csv_outf.writeheader()
		for row in csv_file:
			date_obj = datetime.datetime.strptime(row['committer_dt'], '%Y-%m-%d %H:%M:%S')
			scaled_date = (date_obj-min_date).total_seconds() / total_delta_seconds
			row['committer_dt'] = scaled_date
			row['file_name_index'] = file_name_ids.index(int(row['file_name_id']))
			csv_outf.writerow(row)
			outf.flush()