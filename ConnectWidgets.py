import csv
import math
from collections import defaultdict
from PySide import QtCore, QtGui
from sys import platform as _platform
import weakref
import cProfile

class ConnectWidgets(QtGui.QWidget):
    def __init__(self,widget,Ui, OverviewObject):
        super(ConnectWidgets,self).__init__()

        # Ui.timeline.valueChanged[int].connect(widget.changeTimeline)
        # Ui.range.valueChanged[int].connect(widget.changeRange)