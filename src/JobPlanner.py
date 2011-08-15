import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from TaskWidget import *

class MainWindow(QtGui.QWidget):
    def __init__(self, init_num_task = 3, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.setWindowTitle("Job planner")
        self.tasks_list = []
        self.next_task_id = 0

        self.build_layout()
        self.add_function_buttons()
        self.setup_slots()

        for i in range(0, init_num_task):
            self.add_new_task()

    def task_edited(self, task_id):
        task = self.get_task_by_id(task_id)

        if self.tasks_list[-1] == task:
            self.add_new_task()
            task.setFocus()

        task_index = self.tasks_list.index(task)
        self.tasks_list[task_index+1].setFocus()

    def build_layout(self):
        self.layout = QtGui.QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        #self.layout.setDirection(3)
        self.setLayout(self.layout)
        #self.setStyleSheet("background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #34ABF9, stop: 1 #177BD8);")

    def add_function_buttons(self):
        self.exit_btn = QtGui.QPushButton('Exit')
        self.connect(self.exit_btn, QtCore.SIGNAL('clicked()'), exit)

        self.add_task_btn = QtGui.QPushButton('Add new task')
        self.connect(self.add_task_btn, QtCore.SIGNAL('clicked()'), self.add_new_task)

        #self.layout.addWidget(self.exit_btn)
        self.layout.addWidget(self.add_task_btn)


    def setup_slots(self):
        pass

    def get_task_by_id(self, task_id):
        for task in self.tasks_list:
            if task.id == task_id:
                return task

    def process_remove_task(self, task_id):
        task = self.get_task_by_id(task_id)
        task.hide()
        self.tasks_list.remove(task)
        self.layout.removeWidget(task)
        QtCore.QCoreApplication.sendPostedEvents()
        self.resize(self.minimumSize())
        self.updateGeometry()


    def add_new_task(self):
        task = TaskWidget(self.next_task_id)
        self.layout.addWidget(task)
        self.tasks_list.append(task)
        self.connect(self.tasks_list[len(self.tasks_list)-1].remove_btn, QtCore.SIGNAL('task_removed'), self.process_remove_task)
        self.next_task_id = self.next_task_id + 1
        self.connect(task, QtCore.SIGNAL('textEntered'), self.task_edited)


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


app = QtGui.QApplication(sys.argv)

main_win = MainWindow()
systry = ApplicationSystemTry(main_win)
systry.show()
main_win.show()

sys.exit(app.exec_())

