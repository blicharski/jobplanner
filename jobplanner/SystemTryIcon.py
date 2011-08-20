

class ApplicationSystemTry(QtGui.QSystemTrayIcon):
    def __init__(self, parent = None):
        self.icon = QtGui.QIcon('../img/systray.png')
        QtGui.QSystemTrayIcon.__init__(self, self.icon, parent)
        self.connect(self, QtCore.SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.tray_clicked)
        self.parent = parent
        self.parent_minimized = False
        self.set_parent_window_position()

    def tray_clicked(self, reason):
        if reason == self.Trigger:
            if self.parent_minimized == False:
                self.parent.setVisible(False)
                self.parent_minimized = True
            else:
                self.set_parent_window_position()
                self.parent.setVisible(True)
                self.parent_minimized = False

    def set_parent_window_position(self):
        self.parent.move(self.geometry().x(), self.geometry().y())