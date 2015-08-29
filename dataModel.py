import csv
import sys
import math
import datetime
from collections import defaultdict
from collections import OrderedDict
from PySide import QtCore, QtGui
from sys import platform as _platform
import weakref
import cProfile
import pprint
import os
"""
DataModel is a class where there are setter and getter methods that 
can be called whenever interactive visualizations are initiated in the high_level_view
file. 

This is what I think should be a good idea for a datamodel class 

1) Vishak used his own custom csv reader to implement his own reader specific
functions, this will be really difficult for us as we are dealing dictionary
of dictionary. 
This post is a great for changing this code into a data analysis library Pandas
https://www.airpair.com/python/posts/top-mistakes-python-big-data-analytics
Just look at the part where they say about pandas not into great detail

2) Idea is to feed this function with the relevant data through this class 

    1) The first line of data are the headers so read them and put them in a string data structure,etc
    2) Put all the data in readily available pandas data structure 
        This includes getter and setter functions for 
            1) interpolation_points_time
            2) interpolation_points_author 
            3) ..,etc 
            4) make sure that these functions are extendible as we will many DS
    3) Whatever DS you add make sure that you the DS required to implement this taken care
       line_x_coordinate_begin=min(interpolation_points_time)*length_window
            line_length=max(interpolation_points_time)*length_window-min(interpolation_points_time)*length_window
            #print 'coordinate',line_x_coordinate_begin,line_length
            self.draw_line(event,qp,line_x_coordinate_begin,y_coordinate,line_length,self.height_each_line,interpolation_points_time,interpolation_points_author,author_colors)
            y_coordinate=y_coordinate+10
            counter=counter+1
            data_csv=[row]

    def process_data(self,event,qp,length_window,height_window,height_line,number_authors):
        author_colors=self.author_color_map(number_authors)
        

        data_csv=[]
        flag=0
        y_coordinate=0
        counter=0
        for row in self.csv_rows:
            #omit first line
            if flag == 0:
                flag =1
                continue
            #read only 700 files
            if counter == 700:
                break
            #if this is the first time you are reading, dont check for previous entries
            if len(data_csv)==0:
                data_csv.append(row)
            else:
                #compare if same file commit is seen in the current row as previous row
                #3rd column is file name
                if data_csv[-1][2]==row[2]:
                    data_csv.append(row)
                else:
                    interpolation_points_time=[]
                    interpolation_points_author=[]
                    for x in data_csv:
                        #Assume that interpolation_points =[[x coordinate of interpolation point(compressed to 0-1 scale,author id)]]
                        #coordinate 1, author 0
                        interpolation_points_time.append(float(x[1]))
                        interpolation_points_author.append(int(x[0],10))
                    
                    #define the current line specification
                    line_x_coordinate_begin=min(interpolation_points_time)*length_window
                    line_length=max(interpolation_points_time)*length_window-min(interpolation_points_time)*length_window
                    #print 'coordinate',line_x_coordinate_begin,line_length
                    self.draw_line(event,qp,line_x_coordinate_begin,y_coordinate,line_length,self.height_each_line,interpolation_points_time,interpolation_points_author,author_colors)
                    y_coordinate=y_coordinate+10
                    counter=counter+1
                    data_csv=[row]



4) A very general color generation function that can dynamically generate
visually perceptive and distinct colors in real-time and let the system know

the code in high_level_view that implements it is 

    def author_color_map(self,n):
        HSV_tuples = [(x*1.0/n, 0.9, 0.7) for x in range(n)]
        RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)    
        return RGB_tuples

        where n tells you the number of entities    

"""
class DataModel(QtCore.QObject):
    DataChange = QtCore.Signal(bool)

    def __init__(self,projectname,metrics):
        super(DataModel,self).__init__()
        self.projectname = projectname
        # TODO: we assume the path is data/file. Might want to change that
        # TODO: the better way to do this is to use the raw data (not with modified
        # timestamps and file ids) and convert it in this init function to save
        # a step in generating data.
        self.rawdatafile = 'data/' + projectname + '_git_log_data_wmetrics.csv'
        self.datafile = 'data/' + projectname + '_git_log_data_wmetrics_wauthors_modified_timestamp_fileindex.csv'
        self.bugfile = 'data/' + projectname + '_bug_data.csv'
        # I think the best way to do this is gather all the data for
        # all metrics before hand so we only have to run through
        # each data file once on initialization.
        self.file_blocks = {}
        self.metrics = metrics
        self.sortedDict = []
        self.metrics = {}
        self.MaxMetrics = {} 
        self.file_blocks = dict()
        self.file_blocks_bugs = dict()

        # Deal with general data file
        with open(self.datafile, 'rb') as csvfile:
            csv_file = csv.DictReader(csvfile, delimiter=',')
            print "Loading data......."
            i = 0 
            for row in csv_file:
                i = i + 1
                # if i == 500:
                #     break
                x_coord = float(row['committer_dt'])
                self.metric_values = {metric: row[metric] for metric in metrics}
                self.metric_values['x_coord'] = float(x_coord)
                self.metric_values['committer_contributor_id'] = row['committer_contributor_id']
                if row['file_name_id'] in self.file_blocks.keys():
                    self.file_blocks[row['file_name_id']].append(self.metric_values)
                else:
                    self.file_blocks[row['file_name_id']] = [self.metric_values]
        self.sortIndividualFileIds()
        self.sortRowsByXcoord()
        self.writeToaFile()

        # Deal with bug data file
        # Need to convert dates to indices in accordance to the file above
        self.dates = []
        #self.file_name_ids = []
        self.total_delta_seconds = 0
        self.createIndices(self.rawdatafile)
        # Now create the dictionary
        i =0 
        with open(self.bugfile, 'rb') as csvfile:
            csv_file = csv.DictReader(csvfile, delimiter=',')
            print "Loading bug data......"
            for row in csv_file:
                i = i + 1
                # if i == 500:
                #     break
                intro_date = self.getScaledDate(row['intro_date'])
                fixing_date = self.getScaledDate(row['fixing_date'])
                bug_time = {'intro_date': intro_date, 'fixing_date': fixing_date}
                #file_name_index = self.file_name_ids.index(int(row['file_name_id']))
                if row['file_name_id'] in self.file_blocks_bugs.keys():
                    self.file_blocks_bugs[row['file_name_id']].append(bug_time)
                else:
                    self.file_blocks_bugs[row['file_name_id']] = [bug_time]
        self.writeBugToaFile()
        self.MaxMetrics['committer_contributor_id'] = self.findLengthofMetrics('committer_contributor_id')
        self.MaxMetrics['sumcyclomatic'] = self.findLengthofMetrics('sumcyclomatic')
        self.MaxMetrics['ratiocommenttocode'] = self.findLengthofMetrics('ratiocommenttocode')
        self.MaxMetrics['countlinecode'] = self.findLengthofMetrics('countlinecode')
        self.MaxMetrics['countlinecomment'] = self.findLengthofMetrics('countlinecomment')
        self.MaxMetrics['countlinecodeexe'] = self.findLengthofMetrics('countlinecodeexe')
        self.MaxMetrics['countdeclfunction'] = self.findLengthofMetrics('countdeclfunction')
        self.MaxMetrics['countdeclmethodpublic'] = self.findLengthofMetrics('countdeclmethodpublic')
        self.MaxMetrics['countdeclmethodprivate'] = self.findLengthofMetrics('countdeclmethodprivate')
        self.MaxMetrics['countdeclmethodall'] = self.findLengthofMetrics('countdeclmethodall')
        # pprint.pprint(self.MaxMetrics)
        self.writeMetricToaFile()

    def getScaledDate(self, datestr):
        min_date = min(self.dates)
        max_date = max(self.dates)
        date_obj = datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        total_delta_seconds = (max_date - min_date).total_seconds()
        return (date_obj-min_date).total_seconds() / total_delta_seconds
                 
    def createIndices(self, filen):
        with open(filen, 'rb') as csvfile:
            csv_file = csv.DictReader(csvfile, delimiter=',')
            for row in csv_file:
                self.dates.append(datetime.datetime.strptime(row['committer_dt'], '%Y-%m-%d %H:%M:%S'))
                #self.file_name_ids.append(int(row['file_name_id']))
        #self.file_name_ids = list(set(self.file_name_ids))
        #self.file_name_ids.sort()

    def author_color_map(self,n):
        HSV_tuples = [(x*1.0/n, 0.9, 0.7) for x in range(n)]
        RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)    
        return RGB_tuples

    def sortRowsByXcoord(self):
        self.sortedDict = OrderedDict(sorted(self.file_blocks.items(), key=lambda t: t[1][0]['x_coord'] ))

    def findLengthofMetrics(self,metric):
        Max = 0
        with open(self.datafile , 'rb') as csvfile:
            csv_file = csv.DictReader(csvfile, delimiter=',')
            for row in csv_file:
                try:
                    if Max < float(row[metric]):
                        Max = float(row[metric])
                except ValueError:
                    pass
        return Max

    def sortIndividualFileIds(self):
        for key in self.file_blocks.keys():
            for i in range(len(self.file_blocks[key])):
                    for j in range(i+1,len(self.file_blocks[key])):
                        if float(self.file_blocks[key][j]['x_coord']) < float(self.file_blocks[key][i]['x_coord']):
                            temp = self.file_blocks[key][j]
                            self.file_blocks[key][j] = self.file_blocks[key][i]
                            self.file_blocks[key][i] = temp


    def writeBugToaFile(self):
        import pickle
        print "Writing bug data to a File"
        pprint.pprint(self.file_blocks_bugs)
        with open(self.projectname+'BugData.pickle', 'wb') as handle:
            pickle.dump(self.file_blocks_bugs, handle)

    def writeMetricToaFile(self):
        import pickle
        print "Writing Max to a File"
        with open(self.projectname+'MaxItems.pickle', 'wb') as handle:
            pickle.dump(self.MaxMetrics, handle)

    def writeToaFile(self):
        import pickle
        with open(self.projectname+'.pickle', 'wb') as handle:
            pickle.dump(self.sortedDict, handle)

# # As of 4/9/2015 3:11PM, available metrics are
metrics = ['add_count','del_count','countlinecode',
            'countlinecomment','countlinecodeexe',
            'countdeclfunction','countdeclmethodpublic',
            'countdeclmethodprivate','countdeclmethodall',
            'maxinheritancetree','ratiocommenttocode','sumcyclomatic']

dm = DataModel('qpid' ,metrics)






