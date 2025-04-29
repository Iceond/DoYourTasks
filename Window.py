from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidget, QTabWidget, QLabel, QPushButton, \
    QLineEdit, QListWidget, QComboBox, QGridLayout, QCalendarWidget, QTableWidgetItem
from PySide6.QtGui import QColor,QPalette
import sys
from PySide6.QtCore import Signal
from tables import Create_Task,Drop_Task,Tasks,Get_Category,get_Priority,session


def droptaskbyid(value):
    Drop_Task(value)



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
        self.table.setRowCount(len(rows))

        for row, cols in enumerate(str(rows)):
            for col, text in enumerate(cols):
                print(col)
                self.table.setItem(row, col, QTableWidgetItem(text))
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
        task = self.taskcategory.currentIndex()
        priority = self.taskdifficulty.currentIndex()
        Create_Task(name=name,description="",category=task,priority=priority,due_date="-")
        updateTasks()
    def pressed(self):
         try:
             value = int(self.id.text())
         except Exception as e:
             print(e)
rows = []
def updateTasks():
    tasks = session.query(Tasks).all()
    print(tasks)
    for task in tasks:
        rows.append(task.taskname)
        rows.append(task.description)
        rows.append(task.category_id)
        rows.append(task.priority_id)
        rows.append(task.due_date)
        print(rows)
updateTasks()

app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

main = View_Tasks(rows)
main.show()
app.exec()