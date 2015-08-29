#!/usr/bin/python
# -*- coding: utf-8 -*-
#Creates a high level view of the repository by reading the csv file camel_git_log_modified_time.csv
#refer to initUI function in class where you can modify length/height of window, also width for each line in the visualization (more the files, thinner line should be to accomodate all file)
#Time has been modified in the CSV file - found the oldest time and assigned that value 0(should have 0 as its x coordinate), and most recent is given as 1(1*length will be the  coordinate for that time), remaining times are relative to that.
#color for each author is generated using function author color map 
import sys, random,csv,colorsys
from PySide import QtGui, QtCore, QtUiTools
import pickle
import datetime as dt
import time
import math 
import pprint 
import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from overview import Overview
from SpatiallyConsistant import SpatialOverview
from cveJiraLink import CveJiraLink
import datetime

jet = cm = plt.get_cmap('jet') 
#Importing from classes in the repository  
from Layout import LayoutInit
from ConnectWidgets import ConnectWidgets

metrics = ['add_count','del_count','countlinecode',
        'countlinecomment','countlinecodeexe',
        'countdeclfunction','countdeclmethodpublic',
        'countdeclmethodprivate','countdeclmethodall',
        'maxinheritancetree','ratiocommenttocode','sumcyclomatic']

class VizView(QtGui.QWidget):
    
    LineEditChanged = QtCore.Signal(int)
    PositionChanged = QtCore.Signal(list)
    author_color=None

    def __init__(self,dataModel, MaxMetrics, BugData, projectname):
        super(VizView, self).__init__()
        self.dataModel = dataModel
        self.createDates(projectname)
        self.initUI(dataModel, MaxMetrics, BugData, projectname)
        

    def initUI(self, dataModel, MaxMetrics, BugData, projectname): 
        self.visHeatMap = 'committer_contributor_id'
        self.length_window = 800 
        self.pointer = None
        self.BugDataState = False
        self.height_window = 800
        self.UseMatplotLib = False
        self.BugData =BugData
        self.MaxMetrics = MaxMetrics
        self.distinctAuthorData = self.MaxMetrics['committer_contributor_id'] + 2
        self.height_each_line=float(1)
        self.height_each_line_setting = float(5)
        self.author_colors= self.colo_map(int(self.distinctAuthorData),True)
        self.y_coordinate = 0
        self.dataModel = dataModel
        self.setGeometry(0, 0, self.length_window, self.height_window)
        self.setWindowTitle('Points')
        self.visHeatMap = 'committer_contributor_id'
        self.width = self.determineLineWidth(len(self.dataModel))
        self.setSizePolicy(QtGui.QSizePolicy.Policy.Expanding, QtGui.QSizePolicy.Policy.Expanding)
        
        self.position = [0, 0]
        self.scale = 1
        self.length_cutoff = self.length_window * self.scale
        self.height_each_line = self.height_each_line_setting

        self.default_cve_range = 60
        self.cve_range = self.default_cve_range
        self.cjl = CveJiraLink(projectname,self.default_cve_range)
        self.CveDataState = False
        self.projectname = projectname

    def createDates(self,projectname):
        print 'creating dates for scaling'
        self.dates = []
        with open('data/' + projectname + '_git_log_data_wmetrics.csv', 'rb') as csvfile:
            csv_file = csv.DictReader(csvfile, delimiter=',')
            for row in csv_file:
                self.dates.append(datetime.datetime.strptime(row['committer_dt'], '%Y-%m-%d %H:%M:%S'))
        self.min_date = min(self.dates)
        self.max_date = max(self.dates)

    def getScaledDate(self, datestr):
        date_obj = datetime.datetime.strptime(datestr, '%Y-%m-%d %H:%M:%S')
        total_delta_seconds = (self.max_date - self.min_date).total_seconds()
        return (date_obj-self.min_date).total_seconds() / total_delta_seconds

    def BugDataChanged(self,state):
        if state: 
            self.BugDataState = True
        else: 
            self.BugDataState = False
        self.update()

    def CveDataChanged(self,state):
        if state:
            self.CveDataState = True
        else:
            self.CveDataState = False
        self.update()

    def LineEditChanged(self,value):
        """Handling Line Edit changes"""
        text = (value.encode('ascii','ignore')).replace(' ','')
        # value = float(text)*1000
        self.cur_cve_range = text
        # print text
        self.LineEditChanged.emit(int(value))

    def LineEditReturn(self):
        print 'return pressed in line edit'
        self.cve_range = int(self.cur_cve_range)
        self.cjl = CveJiraLink(self.projectname,self.cve_range)
        self.GenerateDropDown(self.pointer)
        self.update()

    def GenerateDropDown(self, pointer):
        # This is where you add the data Let me know if this will change 
        # along the course of the running the software
        list1 = []
        for cve, bugs in self.cjl.cve_bugs_map.iteritems():
            print cve
            list1.append(self.tr(str(cve)))

        self.selected_cve_id = list1[0] if len(list1) > 0 else ''
        self.bug_within_cve = 0
        self.pointer = pointer
        self.pointer.clear()
        self.pointer.addItems(list1)

    def CVEdropDown(self, CVEdropDown):
        # method that is called for the drop down for CVE data
        self.selected_cve_id = CVEdropDown
        print self.selected_cve_id
        self.bug_within_cve = 0
        self.update()


    def CVEPushButton(self):
        print self.selected_cve_id
        print "In not OVerview"

        bugs = self.cjl.cve_bugs_map[self.selected_cve_id]
        print bugs[self.bug_within_cve]
        if self.CveDataState:
            self.navigateToFile(bugs[self.bug_within_cve]['file_name_id'])
            self.bug_within_cve += 1
            if self.bug_within_cve == len(bugs):
                self.bug_within_cve = 0
            print self.bug_within_cve

    def navigateToFile(self, navfile):
        print 'Navigating to ' + navfile
        ypos = 0
        for filename, Data in self.dataModel.iteritems():
            ypos += 1
            if filename == navfile:
                self.position[1] = ypos * self.height_each_line - (self.height_window / 2)
                self.update()
                break

    def heatMap(self, heatMap):
        start_time1 = time.time()
        visuallyPerceptive = True
        if heatMap == "Author Contribution": 
            self.visHeatMap = 'committer_contributor_id'
            self.distinctAuthorData = self.MaxMetrics['committer_contributor_id']
            visuallyPerceptive = True
        elif heatMap == "ratiocommenttocode":
            self.visHeatMap = 'ratiocommenttocode'
            visuallyPerceptive = False
            self.distinctAuthorData = self.MaxMetrics['ratiocommenttocode']
        elif heatMap == "sumcyclomatic": 
            self.visHeatMap = 'sumcyclomatic'
            self.distinctAuthorData = self.MaxMetrics['sumcyclomatic']
            visuallyPerceptive = True
        elif heatMap == "countlinecode": 
            self.visHeatMap = 'countlinecode'
            self.distinctAuthorData = self.MaxMetrics['countlinecode']
            visuallyPerceptive = True
        elif heatMap == "countlinecomment": 
            self.visHeatMap = 'countlinecomment'
            self.distinctAuthorData = self.MaxMetrics['countlinecomment']
            visuallyPerceptive = True
        elif heatMap == "countlinecodeexe": 
            self.visHeatMap = 'countlinecodeexe'
            self.distinctAuthorData = self.MaxMetrics['countlinecodeexe']
            visuallyPerceptive = True
        elif heatMap == "countdeclfunction": 
            self.distinctAuthorData = self.MaxMetrics['countdeclfunction']
            self.visHeatMap = 'countdeclfunction'
            visuallyPerceptive = True
        elif heatMap == "countdeclmethodpublic": 
            self.distinctAuthorData = self.MaxMetrics['countdeclmethodpublic']
            self.visHeatMap = 'countdeclmethodpublic'
            visuallyPerceptive = True
        elif heatMap == "countdeclmethodprivate": 
            self.distinctAuthorData = self.MaxMetrics['countdeclmethodprivate']
            self.visHeatMap = 'countdeclmethodprivate'
            visuallyPerceptive = True
        elif heatMap == "countdeclmethodall": 
            self.distinctAuthorData = self.MaxMetrics['countdeclmethodall']
            self.visHeatMap = 'countdeclmethodall'
            visuallyPerceptive = True


        if not(visuallyPerceptive): 
            self.UseMatplotLib = True 
            self.author_colors=self.colo_map(int(self.distinctAuthorData),False)
        else: 
            self.UseMatplotLib = False
            self.distinctAuthorData = self.distinctAuthorData+2
            self.author_colors=self.colo_map(int(self.distinctAuthorData),visuallyPerceptive)
        self.update() 
        # print self.visHeatMap
        print("Bug data Load  --- %f seconds ---" % (time.time() - start_time1))

    def Metrics(self,metrics):
        print metrics

    def changeTimeline(self,state):
        print state

    def changeRange(self,state): 
        print state

    def overViewChanged(self,state):
        if state: 
            self.overViewChanged = True
        else: 
            self.overViewChanged = False
        self.update()
        pass

    def colorViewChanged(self):
        print "asdas"


    def determineLineWidth(self,N):
        width = self.height_window / N 
        print max(0.2, float(width))
        return max(0.2, float(width))

    def apacheRepo(self,Apache): 
        print Apache

    def githubRepo(self,gitHub):
        print gitHub


    def process_data(self,event,qp,height_line):
        i =0 
        self.y_coordinate = -self.position[1]
        for filename, Data in self.dataModel.iteritems():
            if self.y_coordinate < 0:
                self.y_coordinate += self.height_each_line
                continue
            if self.y_coordinate > self.height_window:
                break
            self.drawHorizontalLine(event,qp,Data,filename)
            i=i+1
            # self.draw_line(event,qp,line_x_coordinate_begin,y_coordinate,line_length,self.height_each_line,interpolation_points_time,interpolation_points_author,author_colors)


    def drawHorizontalLine(self,event, qp, Data, filename):
        i = 0 
        # iterate over the data to render the lines in the application
        interpolation_points_time = []
        interpolation_points_author = []
        i=0 
        self.y_coordinate += self.height_each_line
        for data in Data: 
                interpolation_points_time.append(data['x_coord'])
                i = i + 1
                empty = False
                if data[self.visHeatMap] == '':
                    empty = True
                if data[self.visHeatMap].find('.')!=-1:  
                    if not empty:
                        interpolation_points_author.append(float(data[self.visHeatMap]))
                    else:
                        if len(interpolation_points_author) == 0:
                            interpolation_points_author.append(0)
                        else:
                            interpolation_points_author.append(interpolation_points_author[len(interpolation_points_author)-1])
                else:
                    if not empty:
                        interpolation_points_author.append(int(data[self.visHeatMap],10))
                    else:
                        if len(interpolation_points_author) == 0:
                            interpolation_points_author.append(0)
                        else:
                            interpolation_points_author.append(interpolation_points_author[len(interpolation_points_author)-1])
        # interpolation_points_time.append(1)
        line_x_coordinate_begin = (interpolation_points_time[0] * self.length_window) - self.position[0]
        line_length = self.length_window - (interpolation_points_time[0] * self.length_window)
        self.draw_line(event,qp,line_x_coordinate_begin*self.scale,self.y_coordinate,float(line_length)*self.scale,float(self.height_each_line),interpolation_points_time,interpolation_points_author,self.author_colors)
    # else:

        if self.BugDataState:
            line_x_coordinate_begin_global = (Data[0]['x_coord'] * self.length_window) - self.position[0]
            line_length = self.length_window - (Data[0]['x_coord'] * self.length_window)
            GrayOutAreas = []
            try: 
                BugIndivData = self.BugData[filename]
                for data in BugIndivData:
                    GrayOutAreas.append((data['intro_date'],data['fixing_date']))
                line_x_coordinate_begin = (Data[0]['x_coord'] * self.length_window) - self.position[0]
                line_length = self.length_window - (Data[0]['x_coord'] * self.length_window)
                self.Bug_draw_line(event,qp,line_x_coordinate_begin_global*self.scale,line_x_coordinate_begin*self.scale,self.y_coordinate,float(line_length)*self.scale,float(self.height_each_line),GrayOutAreas)
            except KeyError: 
                pass

        if self.CveDataState:
            line_x_coordinate_begin_global = (Data[0]['x_coord'] * self.length_window) - self.position[0]
            line_length = self.length_window - (Data[0]['x_coord'] * self.length_window)
            WhiteOutAreas = []
            try: 
                bugs = self.cjl.cve_bugs_map[self.selected_cve_id]
                for bug in bugs:
                    if bug['file_name_id'] == filename:
                        WhiteOutAreas.append((self.getScaledDate(bug['intro_date']),self.getScaledDate(bug['fixing_date'])))

                line_x_coordinate_begin = (Data[0]['x_coord'] * self.length_window) - self.position[0]
                line_length = self.length_window - (Data[0]['x_coord'] * self.length_window)
                self.Cve_draw_line(event,qp,line_x_coordinate_begin_global*self.scale,line_x_coordinate_begin*self.scale,self.y_coordinate,float(line_length)*self.scale,float(self.height_each_line),WhiteOutAreas)

            except KeyError: 
                pass

    def draw_line_debug(self,event,qp,begin_x_coordinate,begin_y_coordinate,length,height):
        qp.setBrush(QtGui.QColor(0,0,0))
        qp.drawRect(QtCore.QRectF(begin_x_coordinate, begin_y_coordinate, length, height))


    def Bug_draw_line(self,event,qp,line_x_coordinate_begin_global,begin_x_coordinate,begin_y_coordinate,length,height,GrayOutAreas):
        #Assume that interpolation_points =[[x coordinate of interpolation point(compressed to 0-1 scale,author id)]]

        color = QtGui.QColor(0,0,0)
        color.setAlpha(45)
        for i,j in GrayOutAreas:
            qp.setPen(QtCore.Qt.black) 
            qp.setBrush(color)
            qp.drawRect(QtCore.QRectF(begin_x_coordinate+i*length, begin_y_coordinate, length*j, height))

    def Cve_draw_line(self,event,qp,line_x_coordinate_begin_global,begin_x_coordinate,begin_y_coordinate,length,height,WhiteOutAreas):
        #Assume that interpolation_points =[[x coordinate of interpolation point(compressed to 0-1 scale,author id)]]
        color = QtGui.QColor(255,255,255)
        color.setAlpha(100)
        for i,j in WhiteOutAreas:
            qp.setPen(QtCore.Qt.red) 
            qp.setBrush(color)
            qp.drawRect(QtCore.QRectF(begin_x_coordinate+i*length, begin_y_coordinate, length*j, height))

    def draw_White_Line(self, event, qp, begin_x_coordinate,begin_y_coordinate,  length, height, color):

        qp.setBrush(QtGui.QColor(color[0],color[1],color[2],color[3]))
        qp.setPen(QtCore.Qt.black)
        qp.drawRect(QtCore.QRectF(begin_x_coordinate, begin_y_coordinate, length, height))

    def colo_map(self,n,visuallyPerceptive):

        if visuallyPerceptive: 
            HSV_tuples = [(x*1.0/n, 0.9, 0.7) for x in range(n)]
            RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)    
            return RGB_tuples
        else: 
            import matplotlib as mpl
            import matplotlib.cm as cm
            norm = mpl.colors.Normalize(vmin=0, vmax=n)
            cmap = cm.Oranges
            m = cm.ScalarMappable(norm=norm, cmap=cmap)
            return m

    def draw_line(self,event,qp,begin_x_coordinate,begin_y_coordinate,length,height,interpolation_points_time,interpolation_points_author,author_colors):
        #Assume that interpolation_points =[[x coordinate of interpolation point(compressed to 0-1 scale,author id)]]
        # print "Printing interpolation_points_author",interpolation_points_author
        linearGrad = QtGui.QLinearGradient(QtCore.QPointF(begin_x_coordinate, begin_y_coordinate), QtCore.QPointF(float(begin_x_coordinate+length), float(begin_y_coordinate+height)))    
        if not(self.UseMatplotLib): 
            for i in range(0,len(interpolation_points_author)):
                r_color=author_colors[interpolation_points_author[i]][0]*255
                g_color=author_colors[interpolation_points_author[i]][1]*255
                b_color=author_colors[interpolation_points_author[i]][2]*255
                linearGrad.setColorAt(interpolation_points_time[i],QtGui.QColor(r_color,g_color,b_color))
        else: 
            for i in range(0,len(interpolation_points_author)):
                color = author_colors.to_rgba(interpolation_points_author[i])
                linearGrad.setColorAt(interpolation_points_time[i],QtGui.QColor(color[0]*255,color[1]*255,color[2]*255))

        qp.setBrush(linearGrad)
        qp.setPen(QtCore.Qt.black)
        #qp.drawRect(begin_x_coordinate, begin_y_coordinate, length, float(height))
        qp.drawRect(QtCore.QRectF(begin_x_coordinate, begin_y_coordinate, length, height))


    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        qp.begin(self)
        # Number of distinct elements that is selected 
        self.process_data(e,qp,self.height_each_line)
        qp.end()        

    def mousePressEvent(self, event):
        self.pressed = event.pos()
        self.anchor = self.position

    def mouseReleaseEvent(self, event):
        self.pressed = None

    def mouseMoveEvent(self, event):
        if self.pressed:
            dx, dy = event.x() - self.pressed.x(), event.y() - self.pressed.y()
            self.position = [self.anchor[0] - dx, self.anchor[1] - dy]
            # self.PositionChanged.emit(self.position)
            self.posBoundsCheckSet()
        # self.PositionChanged.emit(self.position)
        self.repaint()

    def wheelEvent(self, event):
        oldscale = self.scale
        self.scale += event.delta() / 12000.0
        if (self.scale < 0.1):
            self.scale = oldscale
            return

        screenpoint = self.mapFromGlobal(QtGui.QCursor.pos())
        dx, dy = screenpoint.x(), screenpoint.y()
        oldpoint = (screenpoint.x() + self.position[0], screenpoint.y() + self.position[1])
        newpoint = (oldpoint[0] * (self.scale/oldscale),
                    oldpoint[1] * (self.scale/oldscale))
        self.position = [newpoint[0] - dx, newpoint[1] - dy]
        if self.scale == 1.0:
            self.position[0] //= 1
            self.position[1] //= 1
        self.posBoundsCheckSet()
        # print self.scale
        self.height_each_line = self.height_each_line_setting * self.scale
    
        self.repaint()

    def posBoundsCheckSet(self):
        bound_hi_x = self.length_window - (self.length_window / self.scale)
        bound_lo_x = -(self.length_window/2)/self.scale
        bound_lo_y = 0
        
        bound_hi_y = self.scale * len(self.dataModel) + 400/self.scale
        if self.position[0] > bound_hi_x:
            self.position[0] = bound_hi_x

        if self.position[1] < bound_lo_y:
            self.position[1] = bound_lo_y

        
def loadFiles():
    loader = QtUiTools.QUiLoader()
    CURR = os.path.dirname(os.path.realpath(sys.argv[0]))
    ui2 = loader.load(os.path.join(CURR, "widgetsforviz.ui"))
    return ui2

def initialize():
        # As of 4/9/2015 3:11PM, available metrics are
    metrics = ['add_count','del_count','countlinecode',
                'countlinecomment','countlinecodeexe',
                'countdeclfunction','countdeclmethodpublic',
                'countdeclmethodprivate','countdeclmethodall',
                'maxinheritancetree','ratiocommenttocode','sumcyclomatic']

def main():
    app = QtGui.QApplication(sys.argv)
    initialize()


    # Profiling purpose 
    # with PyCallGraph(output=GraphvizOutput()):
    print "Loading data..."
    # start_time1 = time.time()
    projectname = "qpid"
    dataModel = pickle.load(open(projectname+".pickle", "rb"))
    print "Max data..."
    MaxElements = pickle.load(open(projectname+"MaxItems.pickle", "rb"))
    print "Bug data..."
    BugData = pickle.load(open(projectname+"BugData.pickle", "rb"))
    # print("Bug data Load  --- %f seconds ---" % (time.time() - start_time1))
    ex = VizView(dataModel,MaxElements,BugData,projectname)

    ui2 = loadFiles() 
    OverviewObject = Overview(dataModel,MaxElements,BugData,projectname,ex)
    SpatialObject = SpatialOverview(dataModel,MaxElements,BugData,projectname,ex)

    loader = QtUiTools.QUiLoader()
    ui2 = loader.load('./widgetsforviz.ui')

    merge = LayoutInit(ex,ui2,OverviewObject, SpatialObject)
    merge.show()

    sys.exit(app.exec_())
    
if __name__ == '__main__':
    main()
