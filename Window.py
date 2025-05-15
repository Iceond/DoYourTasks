from PySide6.QtWidgets import QWidget, QApplication, QMainWindow, QTableWidget, QTabWidget, QLabel, QPushButton, \
    QLineEdit, QListWidget, QComboBox, QGridLayout, QCalendarWidget, QTableWidgetItem, QColorDialog
from PySide6.QtGui import QColor, QPalette
import sys
import random
from PySide6.QtCore import Signal,QDate,QSettings
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
        label = QLabel("Ваши задачи")
        self.setWindowTitle("Tasks")
        self.top_color = QColor(150, 150, 255)
        self.bottom_color = QColor(135, 0, 120)

        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Задание", "Описание", "Категория", "Приоритет", "Дата окончания", "Номер"])
        self.table.resizeColumnsToContents()
        self.top_color_btn = QPushButton()
        self.bottom_color_btn = QPushButton()
        self.top_color_btn.clicked.connect(lambda: self.pick_color("top"))
        self.bottom_color_btn.clicked.connect(lambda: self.pick_color("bottom"))
        self._update_button_colors()
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate.currentDate())
        button = QPushButton("Завершить задачу по номеру")
        labelid = QLabel("Введите номер задачи:")
        self.settings = QSettings("TaskApp", "ColorPreferences")

        # Load saved colors or defaults
        self.top_color = QColor(self.settings.value("top_color", "#9696ff"))
        self.bottom_color = QColor(self.settings.value("bottom_color", "#870078"))

        # Validate colors
        if not self.top_color.isValid():
            self.top_color = QColor(150, 150, 255)
        if not self.bottom_color.isValid():
            self.bottom_color = QColor(35, 0, 120)

        self.id = QLineEdit()
        self.newtask = QPushButton("Создать задачу")
        self.taskname = QLineEdit()
        self.taskdescription = QLineEdit()
        self.taskcategory = QComboBox()
        self.taskdifficulty = QComboBox()
        self.setStyleSheet("""
            View_Tasks {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(150, 150, 255, 255),
                    stop:1 rgba(135, 0, 120, 255));
            }

            QTableWidget, QLineEdit, QComboBox, QCalendarWidget, QPushButton {
                background-color: rgba(255, 255, 255, 200);
                border: 1px solid rgba(0, 0, 0, 100);
                border-radius: 4px;
                padding: 3px;
            }

            QLabel {
                color: white;
                font-weight: bold;
                font-size: 12pt;
            }

            QHeaderView::section {
                background-color: rgba(200, 200, 255, 150);
                padding: 5px;
            }

            QCalendarWidget QWidget { 
                alternate-background-color: rgba(255, 255, 255, 150); 
            }
        """)

        enter_name = QLabel("Введите название задачи:")
        enter_description = QLabel("Описание:")
        enter_category = QLabel("Выберите категорию:")
        enter_priority = QLabel("Выберите приоритет:")
        enter_due_date = QLabel("Выберите дату окончания:")

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
        layout.addWidget(QLabel("Верх градиента:"), 10, 0)
        layout.addWidget(self.top_color_btn, 10, 1)
        layout.addWidget(QLabel("Низ градиента:"), 11, 0)
        layout.addWidget(self.bottom_color_btn, 11, 1)


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

    def pick_color(self, position):
        color = QColorDialog.getColor()
        if color.isValid():
            if position == "top":
                self.top_color = color
            else:
                self.bottom_color = color
            self._update_button_colors()
            self._apply_styles()

    def _update_button_colors(self):
        self.top_color_btn.setStyleSheet(f"background-color: {self.top_color.name()};")
        self.bottom_color_btn.setStyleSheet(f"background-color: {self.bottom_color.name()};")

    def _apply_styles(self):
        self.setStyleSheet(f"""
              View_Tasks {{
                  background: qlineargradient(
                      spread:pad, x1:0, y1:0, x2:0, y2:1,
                      stop:0 {self.top_color.name()},
                      stop:1 {self.bottom_color.name()});
              }}
              QTableWidget, QLineEdit, QComboBox, QCalendarWidget, QPushButton {{
                  background-color: rgba(255, 255, 255, 200);
                  border: 1px solid rgba(0, 0, 0, 100);
                  border-radius: 4px;
                  padding: 3px;
              }}
              QLabel {{ color: white; font-weight: bold; font-size: 12pt; }}
              QHeaderView::section {{ background-color: rgba(200, 200, 255, 150); padding: 5px; }}
              QCalendarWidget QWidget {{ alternate-background-color: rgba(255, 255, 255, 150); }}
          """)

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

    def closeEvent(self, event):
        # Save colors when window closes
        self.settings.setValue("top_color", self.top_color.name())
        self.settings.setValue("bottom_color", self.bottom_color.name())
        super().closeEvent(event)


rowstest = []
updateTasks()

app = QApplication.instance() or QApplication(sys.argv)
main = View_Tasks(rowstest)
main.show()
app.exec()
