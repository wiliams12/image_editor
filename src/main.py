from functionality import Editor
from PySide6.QtWidgets import QApplication
from main_window import MainWindow
from PySide6.QtGui import QIcon

app = QApplication()

editor = Editor()

window = MainWindow(app, editor)
window.show()

app.exec()

