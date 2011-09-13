
from PyQt4.QtCore import SIGNAL, QCoreApplication
from PyQt4.QtGui import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox, QLabel
from TaskWidget import *


class MainWindow(QWidget):
    def __init__(self, init_num_task = 3, parent = None):
        QWidget.__init__(self, parent)
        self.setWindowTitle("Job planner")
        self.tasks_list = []
        self.next_task_id = 0
        
        self.options_panel = QFrame()
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
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.setLayout(self.layout)
        
        self.options_layout = QHBoxLayout()
        self.options_layout.setSpacing(0)
        self.options_layout.setMargin(0)
        self.options_panel.setLayout(self.options_layout)
        
        #self.setStyleSheet("background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #34ABF9, stop: 1 #177BD8);")

    def build_options_panel(self):
        self.options_layout = QHBoxLayout()
        self.options_layout.setSpacing(0)
        self.options_layout.setMargin(0)

    def add_function_buttons(self):

        self.export_btn = QPushButton('Export')
        self.add_task_btn = QPushButton('Add new task')
        
        self.layout.addWidget(self.options_panel)
        self.options_layout.addWidget(self.add_task_btn)
        self.options_layout.addWidget(self.export_btn)

    def setup_slots(self):
        self.connect(self.export_btn, SIGNAL('clicked()'), self.export)
        self.connect(self.add_task_btn, SIGNAL('clicked()'), self.add_new_task)

    def closeEvent(self, event):
        #reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
        #                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        #if reply == QMessageBox.Yes:
        event.accept()
        #else:
        #    event.ignore()

    def get_task_by_id(self, task_id):
        for task in self.tasks_list:
            if task.id == task_id:
                return task

    def process_remove_task(self, task_id):
        task = self.get_task_by_id(task_id)
        task.hide()
        self.tasks_list.remove(task)
        self.layout.removeWidget(task)
        QCoreApplication.sendPostedEvents()
        self.resize(self.minimumSize())
        self.updateGeometry()

    def add_new_task(self):
        task = TaskWidget(self.next_task_id)
        self.layout.addWidget(task)
        self.tasks_list.append(task)
        self.connect(self.tasks_list[len(self.tasks_list)-1].remove_btn, SIGNAL('task_removed'), self.process_remove_task)
        self.next_task_id = self.next_task_id + 1
        self.connect(task, SIGNAL('textEntered'), self.task_edited)

    def export(self):
        for task in self.tasks_list:
            task = task.extract_task_object()
            print(task)


