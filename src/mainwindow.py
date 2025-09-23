from PySide6.QtWidgets import QMainWindow,QToolBar,QPushButton,QStatusBar

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Image Editor")