from PySide.QtUiTools import QUiLoader
import sys
from PySide.QtGui import QApplication, QLineEdit


def main(argv=None):
    if argv is None:
        argv = sys.argv

    app = QApplication(argv)
    loader = QUiLoader()
    ui = loader.load('softvis.ui')
    print "s"
    ui.show()
    # engine = QScriptEngine()
    return app.exec_()
    

if __name__ == '__main__':
    main()