import csv
import datetime
from collections import defaultdict

# from cveJiraLink import CveJiraLink
# cjl = CveJiraLink('qpid', 180)

class CveJiraLink():

	def __init__(self,projectname,timerange_days):
		self.cvefile = 'data/' + projectname + '_cve_data.csv'
		self.bugfile = 'data/' + projectname + '_bug_data.csv'
		self.timerange_days = datetime.timedelta(days=timerange_days)
		self.cves = []
		self.cve_bugs_map = defaultdict(list)
		print "Populating cve -> bug map at a range of " + str(timerange_days) + " days"
		self.populateMap()

	def populateMap(self):
		with open(self.cvefile, 'rb') as cf:
			cvereader = csv.DictReader(cf, delimiter=',')
			for row in cvereader:
				self.cves.append(row)

		with open(self.bugfile, 'rb') as bf:
			bugreader = csv.DictReader(bf, delimiter=',')
			for row in bugreader:
				fix_date = datetime.date(*map(int, row['fixing_date'].split(' ')[0].split('-')))
				for cve in self.cves:
					cve_dt = datetime.date(*map(int, cve['date_published'].split('-')))
					if fix_date >= cve_dt - self.timerange_days and fix_date <= cve_dt:
						self.cve_bugs_map[cve['cve_id']].append(row)

		for cve, bugs in self.cve_bugs_map.iteritems():
			self.cve_bugs_map[cve] = sorted(bugs, key=lambda k: k['fixing_date'])








