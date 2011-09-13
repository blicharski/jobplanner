

from PyQt4.QtGui import QApplication

from MainWindow import *
from SystemTryIcon import *


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    main_win = MainWindow()
    systry = ApplicationSystemTry(main_win)
    systry.show()
    main_win.show()
    sys.exit(app.exec_())
    


