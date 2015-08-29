import sys, random,csv,colorsys
from PySide import QtGui, QtCore, QtUiTools
import pickle
import datetime 
import time
import math 
import pprint 
import os
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
from cveJiraLink import CveJiraLink


metrics = ['add_count','del_count','countlinecode',
        'countlinecomment','countlinecodeexe',
        'countdeclfunction','countdeclmethodpublic',
        'countdeclmethodprivate','countdeclmethodall',
        'maxinheritancetree','ratiocommenttocode','sumcyclomatic']

class SpatialOverview(QtGui.QWidget):
    author_color=None
    def __init__(self,dataModel, MaxMetrics, BugData, projectname, MainWidget):
        super(SpatialOverview, self).__init__()

        self.dataModel = dataModel
        self.createDates(projectname)
        self.initUI(dataModel, MaxMetrics, BugData, projectname, MainWidget)

    def initUI(self, dataModel, MaxMetrics, BugData, projectname, MainWidget): 
        self.visHeatMap = 'committer_contributor_id'
        self.length_window = 800
        self.pointer = None
        self.BugDataState = False
        self.height_window = 800
        self.UseMatplotLib = False
        self.colorViewChanged = True
        self.BugData =BugData
        self.MaxMetrics = MaxMetrics
        self.distinctAuthorData = self.MaxMetrics['committer_contributor_id'] + 2
        self.height_each_line_setting = float(0.009)
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
        if self.colorViewChanged:
            self.update()

    def colorViewChangedf(self,state):
        if state: 
            self.colorViewChanged = True
        else: 
            selfcolorViewChanged = False
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
        self.cur_cve_range = text

    def LineEditReturn(self):
        print 'return pressed in line edit'
        self.cve_range = int(self.cur_cve_range)
        self.cjl = CveJiraLink(self.projectname,self.cve_range)
        self.GenerateDropDown(self.pointer)
        self.update()

    def GenerateDropDown(self, pointer):
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
        self.selected_cve_id = CVEdropDown
        print self.selected_cve_id
        self.bug_within_cve = 0
        self.update()


    def CVEPushButton(self):
        pass

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
        print("Bug data Load  --- %f seconds ---" % (time.time() - start_time1))

    def Metrics(self,metrics):
        print metrics

    def changeTimeline(self,state):
        print state

    def colorViewChangedf(self,state):
        pass
    def changeRange(self,state): 
        print state

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


        line_x_coordinate_begin = (interpolation_points_time[0] * self.length_window) - self.position[0]
        line_length = self.length_window - (interpolation_points_time[0] * self.length_window)
        self.draw_line(event,qp,line_x_coordinate_begin*self.scale,self.y_coordinate,float(line_length)*self.scale,float(self.height_each_line),interpolation_points_time,interpolation_points_author,self.author_colors)


    def draw_line_debug(self,event,qp,begin_x_coordinate,begin_y_coordinate,length,height):
        qp.setBrush(QtGui.QColor(0,0,0))
        qp.drawRect(QtCore.QRectF(begin_x_coordinate, begin_y_coordinate, length, height))


    def Bug_draw_line(self,event,qp,line_x_coordinate_begin_global,begin_x_coordinate,begin_y_coordinate,length,height,GrayOutAreas):
 
        color = QtGui.QColor(0,0,0)
        color.setAlpha(45)
        for i,j in GrayOutAreas:
            qp.setPen(QtCore.Qt.black) 
            qp.setBrush(color)
            qp.drawRect(QtCore.QRectF(begin_x_coordinate+i*length, begin_y_coordinate, length*j, height))

    def Cve_draw_line(self,event,qp,line_x_coordinate_begin_global,begin_x_coordinate,begin_y_coordinate,length,height,WhiteOutAreas):

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
        qp.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0), 0))        

        rect = QtCore.QRectF(begin_x_coordinate, begin_y_coordinate, length, height)

        qp.drawRect(rect)


    def paintEvent(self, e):
        qp = QtGui.QPainter(self)
        qp.begin(self)
        self.process_data(e,qp,self.height_each_line)
        qp.end()        

    def mousePressEvent(self, event):
        self.pressed = event.pos()
        self.anchor = self.position

    def mouseReleaseEvent(self, event):
        self.pressed = None

    def setPosition(self, Position):
        self.position = Position
        # self.posBoundsCheckSet()
        self.update()

    def mouseMoveEvent(self, event):
        if self.pressed:
            dx, dy = event.x() - self.pressed.x(), event.y() - self.pressed.y()
            self.position = [self.anchor[0] - dx, self.anchor[1] - dy]
            self.posBoundsCheckSet()
        self.repaint()

    def wheelEvent(self, event):
        oldscale = self.scale
        self.scale += event.delta() / 1200.0
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