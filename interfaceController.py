# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'softvis.ui'
#
# Created: Sun Mar  1 17:09:13 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SoftVis(object):
    def setupUi(self, SoftVis):
        # SoftVis.setObjectName(QtCore.QString.fromUtf8("SoftVis"))
        SoftVis.resize(833, 571)
        self.centralWidget = QtGui.QWidget(SoftVis)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setGeometry(QtCore.QRect(620, 0, 211, 511))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.listWidget = QtGui.QListWidget(self.groupBox)
        self.listWidget.setGeometry(QtCore.QRect(0, 20, 211, 192))
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.horizontalSlider = QtGui.QSlider(self.groupBox)
        self.horizontalSlider.setGeometry(QtCore.QRect(80, 180, 121, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName(_fromUtf8("horizontalSlider"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 180, 61, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.comboBox = QtGui.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(80, 150, 104, 26))
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 150, 59, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 59, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalSlider_2 = QtGui.QSlider(self.groupBox)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(80, 110, 111, 22))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName(_fromUtf8("horizontalSlider_2"))
        self.radioButton = QtGui.QRadioButton(self.groupBox)
        self.radioButton.setGeometry(QtCore.QRect(30, 30, 111, 20))
        self.radioButton.setObjectName(_fromUtf8("radioButton"))
        self.radioButton_2 = QtGui.QRadioButton(self.groupBox)
        self.radioButton_2.setGeometry(QtCore.QRect(30, 70, 102, 20))
        self.radioButton_2.setObjectName(_fromUtf8("radioButton_2"))
        SoftVis.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(SoftVis)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 833, 22))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuRepository_Visualization = QtGui.QMenu(self.menuBar)
        self.menuRepository_Visualization.setObjectName(_fromUtf8("menuRepository_Visualization"))
        self.menuBug_data_Visualization = QtGui.QMenu(self.menuBar)
        self.menuBug_data_Visualization.setObjectName(_fromUtf8("menuBug_data_Visualization"))
        SoftVis.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(SoftVis)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        SoftVis.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(SoftVis)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        SoftVis.setStatusBar(self.statusBar)
        self.menuBar.addAction(self.menuRepository_Visualization.menuAction())
        self.menuBar.addAction(self.menuBug_data_Visualization.menuAction())

        self.retranslateUi(SoftVis)
        QtCore.QMetaObject.connectSlotsByName(SoftVis)

    def retranslateUi(self, SoftVis):
        SoftVis.setWindowTitle(_translate("SoftVis", "SoftVis", None))
        self.groupBox.setTitle(_translate("SoftVis", "Controls", None))
        self.label.setText(_translate("SoftVis", "Timeline:", None))
        self.comboBox.setItemText(0, _translate("SoftVis", "Author Contribution", None))
        self.comboBox.setItemText(1, _translate("SoftVis", "CVE data vulnerabilities", None))
        self.comboBox.setItemText(2, _translate("SoftVis", "Release dat", None))
        self.label_2.setText(_translate("SoftVis", "Color:", None))
        self.label_3.setText(_translate("SoftVis", "Range :", None))
        self.radioButton.setText(_translate("SoftVis", "Apache Repo", None))
        self.radioButton_2.setText(_translate("SoftVis", "Github Repo", None))
        self.menuRepository_Visualization.setTitle(_translate("SoftVis", "Repository Visualization", None))
        self.menuBug_data_Visualization.setTitle(_translate("SoftVis", "Bug data Visualization", None))

