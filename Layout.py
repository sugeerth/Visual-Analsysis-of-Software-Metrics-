import csv
import math
from collections import defaultdict
from PySide import QtCore, QtGui
from sys import platform as _platform
import weakref
import cProfile

class LayoutInit(QtGui.QWidget):
    def __init__(self,widget,Ui,OverviewObject, SpatialObject):
        super(LayoutInit,self).__init__()

        widget.setMinimumSize(800, 800)
        Ui.setMinimumSize(250, 550)

        scroll = QtGui.QScrollArea()
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scroll.setWidgetResizable(True)
        scroll.setWidget(widget)


        scrollOverview = QtGui.QScrollArea()
        scrollOverview.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scrollOverview.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scrollOverview.setWidgetResizable(True)
        scrollOverview.setWidget(OverviewObject)


        scrollSpatial = QtGui.QScrollArea()
        scrollSpatial.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scrollSpatial.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        scrollSpatial.setWidgetResizable(True)
        scrollSpatial.setWidget(SpatialObject)

        scroll.setMinimumSize(800, 800)

        hbox = QtGui.QVBoxLayout()
        hbox.addWidget(scroll)
        hbox.setContentsMargins(0, 0, 0, 0)

        hbox1 = QtGui.QVBoxLayout()
        hbox1.addWidget(scrollOverview)
        hbox1.setContentsMargins(0, 0, 0, 0)

        Ui.OverviewWidget.addLayout(hbox1)

        hbox2 = QtGui.QVBoxLayout()
        hbox2.addWidget(scrollSpatial)
        hbox2.setContentsMargins(0, 0, 0, 0)
        Ui.SpatialWidget.addLayout(hbox2)

        Ui.heatMap.activated[str].connect(widget.heatMap)
        Ui.heatMap.activated[str].connect(SpatialObject.heatMap)

        Ui.overView.stateChanged.connect(OverviewObject.overViewChangedf)
        Ui.colorView.stateChanged.connect(SpatialObject.colorViewChangedf)

        Ui.Bugdata.stateChanged.connect(widget.BugDataChanged)
        Ui.Bugdata.stateChanged.connect(OverviewObject.BugDataChanged)
        # Ui.Bugdata.stateChanged.connect(SpatialObject.BugDataChanged)

        Ui.CVEdata.stateChanged.connect(widget.CveDataChanged)
        Ui.CVEdata.stateChanged.connect(OverviewObject.CveDataChanged)
        # Ui.CVEdata.stateChanged.connect(SpatialObject.CveDataChanged)

        # Ui.CVEdataDropdown 
        Ui.pushButton.clicked.connect(widget.CVEPushButton)
        Ui.pushButton.clicked.connect(OverviewObject.CVEPushButton)
        # Ui.pushButton.clicked.connect(SpatialObject.CVEPushButton)

        Ui.textData.setText('60')

        Ui.textData.textChanged.connect(widget.LineEditChanged)
        Ui.textData.textChanged.connect(OverviewObject.LineEditChanged)
        # Ui.textData.textChanged.connect(SpatialObject.LineEditChanged)


        Ui.textData.returnPressed.connect(widget.LineEditReturn)
        Ui.textData.returnPressed.connect(OverviewObject.LineEditReturn)
        # Ui.textData.returnPressed.connect(SpatialObject.LineEditReturn)


        widget.GenerateDropDown(Ui.CVEdataDropdown)
        OverviewObject.GenerateDropDown(Ui.CVEdataDropdown)
        SpatialObject.GenerateDropDown(Ui.CVEdataDropdown)


        Ui.CVEdataDropdown.activated[str].connect(widget.CVEdropDown) 
        Ui.CVEdataDropdown.activated[str].connect(OverviewObject.CVEdropDown) 
        # Ui.CVEdataDropdown.activated[str].connect(SpatialObject.CVEdropDown) 


        # connecting widgets 
        widget.PositionChanged.connect(SpatialObject.setPosition)


        bbbox = QtGui.QHBoxLayout()
        bbbox.addWidget(Ui)
        bbbox.addLayout(hbox)
        bbbox.setContentsMargins(0, 0, 0, 0)

        self.setLayout(bbbox)

