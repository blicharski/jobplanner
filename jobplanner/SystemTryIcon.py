
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QSystemTrayIcon, QIcon
from ResourceManager import resourceManager

class ApplicationSystemTry(QSystemTrayIcon):
    def __init__(self, parent = None):
        self.icon = QIcon(resourceManager.get_image("systray"))
        QSystemTrayIcon.__init__(self, self.icon, parent)
        self.connect(self, SIGNAL('activated(QSystemTrayIcon::ActivationReason)'), self.tray_clicked)
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
