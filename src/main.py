from functionality import Editor
from PySide6.QtWidgets import QApplication
from main_window import MainWindow

app = QApplication()

editor = Editor()

window = MainWindow(app, editor)
window.show()

app.exec()

