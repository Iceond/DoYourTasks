from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidget, QTabWidget, QLabel, QPushButton, \
    QLineEdit, QListWidget, QComboBox, QGridLayout, QCalendarWidget, QTableWidgetItem
from PySide6.QtGui import QColor,QPalette
import sys
import random
from PySide6.QtCore import Signal
from tables import Create_Task, Drop_Task, Tasks, Get_Category, get_Priority, session, getcategorybyid


def droptaskbyid(value):
    Drop_Task(value)
def updateTasks():
    tasks = session.query(Tasks).all()
    print(tasks)
    for task in tasks:
        rowstest.append(task.taskname)
        rowstest.append(task.description)
        rowstest.append(getcategorybyid(task.category_id))
        rowstest.append(task.priority_id)
        rowstest.append(task.due_date)
        print(rowstest)


class View_Tasks(QWidget):
    def __init__(self,rows):
        super().__init__()
        value = ""

        self.resize(600,800)
        label = QLabel("Your Tasks")
        self.table = QTableWidget()  # 3 строк, 3 столбца
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["","Задание", "Описание", "Категория","Приоритет","Дата окончания"])
        self.table.setVerticalHeaderLabels(["1", "2", "3"])
        self.table.resizeColumnsToContents()
        self.table.setRowCount(len(rowstest))
        #for col in range(1,6):
        #    for row in range(0,len(rowstest)):
        #        self.table.setItem(row,col,QTableWidgetItem(str(rowstest[0])))
        # FIX!!!!!!!!!!!!!!!!

        button = QPushButton("Complete Task")
        labelid = QLabel("enter ID:")
        self.id = QLineEdit()
        self.newtask = QPushButton("Create Task")
        self.taskname = QLineEdit()
        self.taskcategory = QComboBox()
        self.taskdifficulty = QComboBox()
        enter_name = QLabel("Enter Name:")
        item = get_Priority()
        item2 = Get_Category()
        enter_category = QLabel("Enter Category:")
        enter_priority = QLabel("Enter Priority:")
        self.taskcategory.addItems(item2)
        self.taskdifficulty.addItems(item)

        button.clicked.connect(droptaskbyid)
        layout = QGridLayout()
        layout.addWidget(label)
        layout.addWidget(self.table)
        layout.addWidget(labelid)
        layout.addWidget(self.id)
        layout.addWidget(button)
        layout.addWidget(enter_name)
        layout.addWidget(self.taskname)
        layout.addWidget(enter_category)
        layout.addWidget(self.taskcategory)
        layout.addWidget(enter_priority)
        layout.addWidget(self.taskdifficulty)
        layout.addWidget(self.newtask)
        self.newtask.clicked.connect(self.createTask)
        self.setLayout(layout)
        #self.id.textChanged.connect(self.pressed())


    def createTask(self):
        name = str(self.taskname.text())
        task = self.taskcategory.currentIndex() + 1
        priority = self.taskdifficulty.currentIndex() + 1
        Create_Task(name=name,description="",category=task,priority=priority,due_date="-")
        updateTasks()
    def pressed(self):
         try:
             value = int(self.id.text())
         except Exception as e:
             print(e)
rowstest = []

updateTasks()

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)
main = View_Tasks(rowstest)
main.show()
app.exec()