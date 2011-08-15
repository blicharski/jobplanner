from PyQt4 import QtGui
from PyQt4 import QtCore
from threading import Timer

class TaskRemove(QtGui.QPushButton):
    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.id = id
        self.button_clicked = 0
        self.icon_changer_timer = None
        self.setMaximumSize(25, 25)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setStyleSheet(
          "background-image: url(../img/delete.png);"
          "background-repeat:no-repeat;"
        )

        self.connect(self, QtCore.SIGNAL('clicked()'), self.on_remove)
        self.connect(self, QtCore.SIGNAL('cancel_delete'), self.cancel_delete)

    def send_cancel_delete_signal(self):
        self.emit(QtCore.SIGNAL('cancel_delete'), ())

    def cancel_delete(self):
        self.button_clicked = 0
        self.icon_changer_timer.cancel()
        self.setStyleSheet("background-image: url(../img/delete.png);")

    def on_remove(self):
        if self.button_clicked == 0:
            self.setStyleSheet("background-image: url(../img/delete_confirm.png);")
            self.button_clicked = 1
            self.icon_changer_timer = Timer(1, self.send_cancel_delete_signal)
            self.icon_changer_timer.start()
        else:
            self.icon_changer_timer.cancel()
            self.emit(QtCore.SIGNAL('task_removed'), (self.id))


class TaskAccept(QtGui.QPushButton):
    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.id = id
        self.setMaximumSize(25, 25)
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setStyleSheet(
          "background-image: url(../img/accept.png);"
          "background-repeat:no-repeat;"
        )

class TaskTimePanel(QtGui.QFrame):
    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setMargin(0)



class TaskEdit(QtGui.QLineEdit):
    minimum_width = 10 # Minimum width in chars

    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.id = id
        self.setMinimumWidth(QtGui.QFontMetrics(self.font()).maxWidth()
                             * self.minimum_width)
        #self.setStyleSheet(
        #    "background-color: white;"
        #)
        self.setup_signals()

    def setup_signals(self):
        pass

class TaskWidget(QtGui.QFrame):
    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.id = id
        self.greened = False
        self.remove_btn = TaskRemove(id)
        self.edit_btn = TaskEdit(id)
        self.accept_btn = TaskAccept(id)

        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setMargin(0)

        self.layout.addWidget(self.remove_btn)
        self.layout.addWidget(self.edit_btn)
        self.layout.addWidget(self.accept_btn)

        self.setLayout(self.layout)
        self.setup_signals()

    def setup_signals(self):
        self.connect(self.accept_btn, QtCore.SIGNAL('clicked()'), self.on_accept)
        self.connect(self.edit_btn, QtCore.SIGNAL('returnPressed()'), self.emit_text_entered)

    def emit_text_entered(self):
        self.emit(QtCore.SIGNAL('textEntered'), (self.id))

    def setFocus(self):
        self.edit_btn.setFocus()

    def on_accept(self):
        if self.greened == False:
            self.edit_btn.setStyleSheet(
                "background-color: green;"
                "color: white;"
                )
            self.greened = True
        else:
            self.edit_btn.setStyleSheet(
                "background-color: white;"
                "color: black;"
                )
            self.greened = False

