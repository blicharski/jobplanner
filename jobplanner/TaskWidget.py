from PyQt4 import QtGui
from PyQt4 import QtCore
from threading import Timer
from ResourceManager import *

class TaskRemove(QtGui.QPushButton):
    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.id = id
        self.button_clicked = 0
        self.icon_changer_timer = None
        self.setMaximumSize(resourceManager.get_icon_image_max_size())
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setStyleSheet(
          "background-image: url(" + resourceManager.get_image('delete') + ");"
          "background-repeat:no-repeat;"
        )

        self.connect(self, QtCore.SIGNAL('clicked()'), self.on_remove)
        self.connect(self, QtCore.SIGNAL('cancel_delete'), self.cancel_delete)

    def send_cancel_delete_signal(self):
        self.emit(QtCore.SIGNAL('cancel_delete'), ())

    def cancel_delete(self):
        self.button_clicked = 0
        self.icon_changer_timer.cancel()
        self.setStyleSheet("background-image: url(" + resourceManager.get_image('delete') + ");")

    def on_remove(self):
        if self.button_clicked == 0:
            self.setStyleSheet("background-image: url(" + resourceManager.get_image('delete_confirm') + ");")
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
        self.setMaximumSize(resourceManager.get_icon_image_max_size())
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setStyleSheet(
          "background-image: url(" + resourceManager.get_image('accept') + ");"
          "background-repeat:no-repeat;"
        )

class TaskClock(QtGui.QPushButton):
    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.setMaximumSize(resourceManager.get_icon_image_max_size())
        self.setStyleSheet(
          "background-image: url(" + resourceManager.get_image('clock') + ");"
          "background-repeat:no-repeat;"
        )

class TaskEdit(QtGui.QLineEdit):
    minimum_width = 10 # Minimum width in chars

    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.id = id
        self.setMinimumWidth(resourceManager.get_widthest_char_size(self)
                             * self.minimum_width)
        #self.setStyleSheet(
        #    "background-color: white;"
        #)


class TimeEdit(QtGui.QFrame):
    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.hour_from = QtGui.QLineEdit(self)
        self.init_entry(self.hour_from)
        self.hour_to   = QtGui.QLineEdit(self)
        self.init_entry(self.hour_to)
        self.hours_count = QtGui.QLineEdit(self)
        self.init_entry(self.hours_count)
        
        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setMargin(0)

        self.layout.addWidget(self.hour_from)
        self.layout.addWidget(self.hour_to)
        self.layout.addWidget(self.hours_count)

        self.setLayout(self.layout)

        self.hours_count.focusInEvent = self.hours_count_focusEvent

    def hours_count_focusEvent(self, event):
        hour_from = self.hour_from.text()
        hour_to   = self.hour_to.text()
        if hour_from != "" and hour_to != "":
            import re
            if re.search(":", hour_from) == None:
                hour_from = hour_from + ":0"
            if re.search(":", hour_to) == None:
                hour_to = hour_to + ":0"
            
            [hour_earlier, min_earlier] = hour_from.split(":")
            [hour_later, min_later]   = hour_to.split(":")

            hour_earlier = int(hour_earlier)
            min_earlier = int(min_earlier)
            hour_later = int(hour_later)
            min_later = int(min_later)
            
            hours_count = hour_later - hour_earlier
            mins_count  = min_later - min_earlier
            if mins_count < 0:
                mins_count = 60 - min_earlier + min_later
                hours_count = hours_count - 1

            self.hours_count.setText(str(hours_count) + "." + str(mins_count))
        
        event.accept()

    def init_entry(self, entry):
        entry.setAlignment(QtCore.Qt.AlignCenter)
        entry.setMaxLength(5)
        entry.setMinimumWidth(resourceManager.get_widthest_char_size(entry) * 3)
        entry.setMaximumWidth(resourceManager.get_widthest_char_size(entry) * 3)
        

    def count_hours(self):
        hour_start = self.hour_from.displayText()
        print("XXXXX" + hour_start)


class TaskWidget(QtGui.QFrame):
    def __init__(self, id, parent = None):
        QtGui.QWidget.__init__(self, parent)

        self.id = id
        self.greened = False
        self.remove_btn = TaskRemove(id)
        self.edit_btn = TaskEdit(id)
        self.accept_btn = TaskAccept(id)
        self.time_btn = TimeEdit(id)
        #self.clock_btn = TaskClock(id)

        self.layout = QtGui.QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setMargin(0)

        self.layout.addWidget(self.remove_btn)
        self.layout.addWidget(self.edit_btn)
        self.layout.addWidget(self.accept_btn)
        self.layout.addWidget(self.time_btn)
        #self.layout.addWidget(self.clock_btn)

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

