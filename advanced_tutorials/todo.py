import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QLineEdit, QListWidget, QMessageBox, QDialog, QLabel
from PyQt6.QtGui import QIcon
import sqlite3
from qt_material import apply_stylesheet

class EditTaskDialog(QDialog):
    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.task = task
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Edit Task')
        self.setGeometry(150, 150, 300, 100)

        self.layout = QVBoxLayout()

        self.label = QLabel('Edit the selected task:', self)
        self.layout.addWidget(self.label)

        self.taskInput = QLineEdit(self)
        self.taskInput.setText(self.task)
        self.layout.addWidget(self.taskInput)

        self.saveButton = QPushButton('Save', self)
        self.saveButton.clicked.connect(self.saveTask)
        self.layout.addWidget(self.saveButton)

        self.setLayout(self.layout)

    def saveTask(self):
        self.task = self.taskInput.text()
        self.accept()

class AssignTaskDialog(QDialog):
    def __init__(self, task_id, parent=None):
        super().__init__(parent)
        self.task_id = task_id
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Assign Task')
        self.setGeometry(150, 150, 300, 150)

        self.layout = QVBoxLayout()

        self.label = QLabel('Assign to:', self)
        self.layout.addWidget(self.label)

        self.personInput = QLineEdit(self)
        self.layout.addWidget(self.personInput)

        self.assignButton = QPushButton('Assign', self)
        self.assignButton.clicked.connect(self.assignTask)
        self.layout.addWidget(self.assignButton)

        self.setLayout(self.layout)

    def assignTask(self):
        person_name = self.personInput.text()
        if person_name:
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute('SELECT id FROM people WHERE name = ?', (person_name,))
            person = c.fetchone()
            if person is None:
                c.execute('INSERT INTO people (name) VALUES (?)', (person_name,))
                conn.commit()
                person_id = c.lastrowid
            else:
                person_id = person[0]
            c.execute('UPDATE tasks SET person_id = ? WHERE id = ?', (person_id, self.task_id))
            conn.commit()
            conn.close()
            self.accept()
        else:
            QMessageBox.warning(self, 'Warning', 'Person name cannot be empty')

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('To-Do App')
        self.setGeometry(100, 100, 600, 400)

        self.mainLayout = QHBoxLayout()

        self.buttonLayout = QVBoxLayout()

        self.addButton = QPushButton('Add Task', self)
        self.addButton.setIcon(QIcon.fromTheme("list-add"))
        self.addButton.clicked.connect(self.addTask)
        self.buttonLayout.addWidget(self.addButton)

        self.editButton = QPushButton('Edit Task', self)
        self.editButton.setIcon(QIcon.fromTheme("document-edit"))
        self.editButton.clicked.connect(self.editTask)
        self.buttonLayout.addWidget(self.editButton)

        self.assignButton = QPushButton('Assign To', self)
        self.assignButton.setIcon(QIcon.fromTheme("user-group-new"))
        self.assignButton.clicked.connect(self.assignTask)
        self.buttonLayout.addWidget(self.assignButton)

        self.deleteButton = QPushButton('Delete Task', self)
        self.deleteButton.setIcon(QIcon.fromTheme("edit-delete"))
        self.deleteButton.clicked.connect(self.deleteTask)
        self.buttonLayout.addWidget(self.deleteButton)

        self.toggleButton = QPushButton('Toggle Dark/Light Mode', self)
        self.toggleButton.setIcon(QIcon.fromTheme("view-refresh"))
        self.toggleButton.clicked.connect(self.toggleMode)
        self.buttonLayout.addWidget(self.toggleButton)

        self.mainLayout.addLayout(self.buttonLayout)

        self.taskLayout = QVBoxLayout()

        self.taskInput = QLineEdit(self)
        self.taskLayout.addWidget(self.taskInput)

        self.taskList = QListWidget(self)
        self.taskLayout.addWidget(self.taskList)

        self.mainLayout.addLayout(self.taskLayout)

        self.setLayout(self.mainLayout)
        self.loadTasks()

        self.lightMode = True
        self.applyStylesheet()

    def applyStylesheet(self):
        if self.lightMode:
            apply_stylesheet(app, theme='light_teal.xml')
        else:
            apply_stylesheet(app, theme='dark_teal.xml')

        self.setStyleSheet("""
            QPushButton {
                border-radius: 15px;
                padding: 10px;
                font-size: 14px;
            }
            QLineEdit {
                padding: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QListWidget {
                padding: 5px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
        """)

    def toggleMode(self):
        self.lightMode = not self.lightMode
        self.applyStylesheet()

    def loadTasks(self):
        conn = sqlite3.connect('todo.db')
        c = conn.cursor()
        c.execute('''SELECT tasks.id, tasks.task, people.name 
                     FROM tasks LEFT JOIN people ON tasks.person_id = people.id''')
        tasks = c.fetchall()
        conn.close()

        self.taskList.clear()
        for task in tasks:
            task_text = task[1]
            if task[2]:
                task_text += f" (Assigned to: {task[2]})"
            self.taskList.addItem(task_text)

    def addTask(self):
        task = self.taskInput.text()
        if task:
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
            conn.commit()
            conn.close()
            self.taskInput.clear()
            self.loadTasks()
        else:
            QMessageBox.warning(self, 'Warning', 'Task cannot be empty')

    def editTask(self):
        selectedTask = self.taskList.currentItem()
        if selectedTask:
            task_text = selectedTask.text().split(" (Assigned to:")[0]
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute('SELECT id FROM tasks WHERE task = ?', (task_text,))
            task_id = c.fetchone()[0]
            conn.close()
            dialog = EditTaskDialog(task_text, self)
            if dialog.exec():
                newTask = dialog.task
                conn = sqlite3.connect('todo.db')
                c = conn.cursor()
                c.execute('UPDATE tasks SET task = ? WHERE id = ?', (newTask, task_id))
                conn.commit()
                conn.close()
                self.loadTasks()
        else:
            QMessageBox.warning(self, 'Warning', 'No task selected')

    def assignTask(self):
        selectedTask = self.taskList.currentItem()
        if selectedTask:
            task_text = selectedTask.text().split(" (Assigned to:")[0]
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute('SELECT id FROM tasks WHERE task = ?', (task_text,))
            task_id = c.fetchone()[0]
            conn.close()
            dialog = AssignTaskDialog(task_id, self)
            if dialog.exec():
                self.loadTasks()
        else:
            QMessageBox.warning(self, 'Warning', 'No task selected')

    def deleteTask(self):
        selectedTask = self.taskList.currentItem()
        if selectedTask:
            task = selectedTask.text().split(" (Assigned to:")[0]
            conn = sqlite3.connect('todo.db')
            c = conn.cursor()
            c.execute('DELETE FROM tasks WHERE task = ?', (task,))
            conn.commit()
            conn.close()
            self.loadTasks()
        else:
            QMessageBox.warning(self, 'Warning', 'No task selected')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = TodoApp()
    ex.show()
    sys.exit(app.exec())
