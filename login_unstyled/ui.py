import sys
from PyQt6.QtWidgets import QApplication,  QWidget, QLabel, QLineEdit, QPushButton,  QVBoxLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

"""
Create a class that represents the Main Login Window
Notice that MainWindow() contains a 'parameter' called QWidget. This is how you use class inheritance.
MainWindow will therefore be able to access anything that QWidget can do, and in fact will be of type QWidget. 
"""
class MainWindow(QWidget):
    def __init__(self, *args, **kwargs):
        """
        We initialize or construct the MainWindow object here by declaring what we need for it to exist.
        *args is an argument that takes positioned, non-keyword arguments as parameters,
            for example, from a previous exercise, we have Circle(5, 'green') where 5 is an int radius and 'green' is
            a colour string; and we list them in that order to draw a green circle object. However, Circle('green', 5)
            would not necessarily work because the positions are now incorrect.

        **kwargs is another argument similar to *args, except that it 'unpacks' from a keyed (remember dictionary keys?)
            list of arguments. Taking the same example as before, Circle(radius=5, color='green') would be a version of
            that object where we now represent the values we feed the initializer. In fact, by using keys, we now can
            even swap the positions since the constructor can actually identify which parameter belongs to which argument
            ie Circle(color='green', radius=5) would still work!
        """
        super().__init__(*args, **kwargs)
        # by calling the super() argument, we say we want the constructor to inherit all arguments from the QWidget class
        self.setWindowTitle('Login') # set the window title, using self, remember we have inherited all parameters from QWidget
        self.setWindowIcon(QIcon('./assets/logo.png')) # same as title, except we can declare an image as our icon

        layout = QVBoxLayout()
        """
        Always declare a layout objet for your window. Here we use QVBoxLayout, which is a Linear Vertical Layout (think column).
        There are others - check out https://www.pythonguis.com/tutorials/pyqt6-layouts/ for more help on layouts!
        For other windows, you might want to use QGridLayout. 
        
        """
        self.setLayout(layout) # setLayout adds the layout object we created above and tells the QWidget superclass what we intend for our GUI to look like

        heading = QLabel(
            'Welcome Back',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        heading.setObjectName('heading')

        subheading = QLabel(
            'Please enter your email and password to log in.',
            alignment=Qt.AlignmentFlag.AlignHCenter
        )
        subheading.setObjectName('subheading')

        self.email = QLineEdit(self)
        self.email.setPlaceholderText('Enter your email')

        self.password = QLineEdit(self)
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setPlaceholderText('Enter your password')

        self.btn_login = QPushButton('Login')

        layout.addStretch()
        layout.addWidget(heading)
        layout.addWidget(subheading)
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password)
        layout.addWidget(self.btn_login)
        layout.addStretch()

        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())