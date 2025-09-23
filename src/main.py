from functionality import Editor
from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

app = QApplication()
editor = Editor()

window = MainWindow(app)
window.show()

app.exec()

