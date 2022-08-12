import sys
from PyQt5 import QtWidgets
import mainWindow

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    win = mainWindow.MainWindow()
    
    win.show()
    
    ret = app.exec_()
    
    sys.exit(ret)

