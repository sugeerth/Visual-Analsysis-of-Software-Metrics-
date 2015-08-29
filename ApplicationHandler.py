import sys, random,csv,colorsys
from PySide import QtGui, QtCore
import datetime as dt
from high_level_view import VizView
from interfaceController import Ui_SoftVis
from PySide import QtCore, QtGui, QtUiTools
import sys
from PyQt4 import QtGui

app = QtGui.QApplication(sys.argv)
loader =  QtUiTools.QUiLoader()
Ui = loader.load('/Users/sugeerthmurugesan/ReposToWork/Research/widgetsforviz.ui')
Ui.show()

# def main(argv=None):
# 	# app = QtGui.QApplication(sys.argv)
# 	if argv is None:
# 		argv = sys.argv
# 	app = QtGui.QApplication(argv)
# 	loader =  QtUiTools.QUiLoader()
# 	Ui = loader.load('/Users/sugeerthmurugesan/ReposToWork/Research/widgetsforviz.ui')
# 	Ui.show()
# 	# Controller = Editor()
# 	# import PySide
# 	# myWidget.show()
# 	# viz = VizView()
# 	# applicationWidget =QtGui.QWidget()

# 	# Box = QtGui.QHBoxLayout()
# 	# Box.addWidget(viz)

# 	# applicationWidget.setLayout(Box)
# 	# applicationWidget.show()


# 	# sys.exit(app.exec_())

# if __name__ == '__main__':
#     main()


# class MainWindow(QtGui.QMainWindow):
#     def __init__(self):
#         QtGui.QMainWindow.__init__(self)
#         self.ui = Ui_SoftVis()
#         self.ui.setupUi(self)
#         self.ui.show()

# # app = QtGui.QApplication(sys.argv)

# # viz = VizView()

# # applicationWidget =QtGui.QWidget()


# # Box = QtGui.QHBoxLayout()
# # Box.addWidget(viz)

# # applicationWidget.setLayout(Box)
# # applicationWidget.show()
# # controller = Ui_SoftVis.setupUi()

# # controller.show()
# # sys.exit(app.exec_())


# if __name__ == '__main__':
#     import sys
#     app = QtGui.QApplication(sys.argv)
#     window = MainWindow()
#     window.show()
#     sys.exit(app.exec_())