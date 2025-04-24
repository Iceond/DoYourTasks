from PySide6.QtWidgets import QWidget,QApplication,QMainWindow, QTableWidget,QTabWidget,QLabel,QPushButton,QLineEdit,QListWidget,QComboBox,QHBoxLayout,QCalendarWidget
from PySide6.QtGui import QColor,QPalette
import sys
from PySide6.QtCore import Signal
from tables import Create_Task,Drop_Task,Tasks


def droptaskbyid(value):
    Drop_Task(value)


class View_Tasks(QWidget):
    def __init__(self):
        super().__init__()
        value = ""
        self.resize(600,800)
        label = QLabel("Your Tasks")
        self.table = QTableWidget(3, 5)  # 3 строк, 3 столбца
        self.table.setHorizontalHeaderLabels(["","Задание", "Описание", "Категория","Приоритет"])
        self.table.setVerticalHeaderLabels(["1", "2", "3"])
        self.table.resizeColumnsToContents()
        button = QPushButton("Complete Task")
        labelid = QLabel("enter ID:")
        self.id = QLineEdit()

        button.clicked.connect(droptaskbyid)
        layout = QHBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.table)
        layout.addWidget(button)
        self.setLayout(layout)
        #self.id.textChanged.connect(self.pressed())
    def pressed(self):
         try:
             value = int(self.id.text())
         except Exception as e:
             print(e)


app = QApplication.instance()
if app is None:
    app = QApplication(sys.argv)

main = View_Tasks()
main.show()
app.exec()