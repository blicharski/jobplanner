import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from JobPlanner import *


app = QtGui.QApplication(sys.argv)

main_win = MainWindow()
systry = ApplicationSystemTry(main_win)
systry.show()
main_win.show()

sys.exit(app.exec_())



