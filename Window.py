from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidget, QTabWidget, QLabel, QPushButton, \
    QLineEdit, QListWidget, QComboBox, QGridLayout, QCalendarWidget, QTableWidgetItem
from PySide6.QtGui import QColor, QPalette
import sys
import random
from PySide6.QtCore import Signal,QDate
from tables import Create_Task, Drop_Task, Tasks, Get_Category, get_Priority, session, getcategorybyid, \
    get_priority_by_id


def updateTasks():
    tasks = session.query(Tasks).all()
    rowstest.clear()
    for task in tasks:
        row = [
            task.taskname,
            task.description,
            getcategorybyid(task.category_id),
            get_priority_by_id(task.priority_id),
            task.due_date,
            task.Id
        ]
        rowstest.append(row)


class View_Tasks(QWidget):
    def __init__(self, rows):
        super().__init__()
        self.resize(600, 800)
        label = QLabel("Your Tasks")
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Задание", "Описание", "Категория", "Приоритет", "Дата окончания", "ID"])
        self.table.resizeColumnsToContents()

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate.currentDate())
        button = QPushButton("Complete Task")
        labelid = QLabel("Enter ID:")
        self.id = QLineEdit()
        self.newtask = QPushButton("Create Task")
        self.taskname = QLineEdit()
        self.taskdescription = QLineEdit()
        self.taskcategory = QComboBox()
        self.taskdifficulty = QComboBox()

        enter_name = QLabel("Enter Name:")
        enter_description = QLabel("Enter Description:")
        enter_category = QLabel("Enter Category:")
        enter_priority = QLabel("Enter Priority:")
        enter_due_date = QLabel("Select Due Date:")

        self.taskcategory.addItems(Get_Category())
        self.taskdifficulty.addItems(get_Priority())

        button.clicked.connect(self.droptaskbyid)
        layout = QGridLayout()
        layout.addWidget(label, 0, 0, 1, 2)
        layout.addWidget(self.table, 1, 0, 1, 2)
        layout.addWidget(labelid, 2, 0)
        layout.addWidget(self.id, 2, 1)
        layout.addWidget(button, 3, 0, 1, 2)
        layout.addWidget(enter_name, 4, 0)
        layout.addWidget(self.taskname, 4, 1)
        layout.addWidget(enter_description, 5, 0)
        layout.addWidget(self.taskdescription, 5, 1)
        layout.addWidget(enter_category, 6, 0)
        layout.addWidget(self.taskcategory, 6, 1)
        layout.addWidget(enter_priority, 7, 0)
        layout.addWidget(self.taskdifficulty, 7, 1)
        layout.addWidget(enter_due_date, 8, 0)
        layout.addWidget(self.calendar, 8, 1)
        layout.addWidget(self.newtask, 9, 0, 1, 2)

        self.newtask.clicked.connect(self.createTask)
        self.setLayout(layout)
        self.refreshTable()

    def refreshTable(self):
        self.table.setRowCount(len(rowstest))
        for row in range(len(rowstest)):
            for col in range(len(rowstest[row])):
                item = QTableWidgetItem(str(rowstest[row][col]))
                self.table.setItem(row, col, item)
        self.table.resizeColumnsToContents()

    def droptaskbyid(self):
        try:
            task_id = int(self.id.text())
            Drop_Task(task_id)
            updateTasks()
            self.refreshTable()
        except ValueError:
            print("Invalid ID")

    def createTask(self):
        name = self.taskname.text()
        selected_date = self.calendar.selectedDate()
        due_date = selected_date.toString("yyyy-MM-dd")
        description = self.taskdescription.text()
        category = self.taskcategory.currentIndex() + 1
        priority = self.taskdifficulty.currentIndex() + 1
        Create_Task(name=name, description=description, category=category, priority=priority, due_date=due_date)
        self.taskname.clear()
        self.calendar.setSelectedDate(QDate.currentDate())
        self.taskdescription.clear()
        updateTasks()
        self.refreshTable()


rowstest = []
updateTasks()

app = QApplication.instance() or QApplication(sys.argv)
main = View_Tasks(rowstest)
main.show()
app.exec()
