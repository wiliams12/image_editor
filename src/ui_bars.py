from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QMenuBar, QToolBar,
    QStatusBar, QLabel, QFrame, QFileDialog, QPushButton
)

from PySide6.QtGui import QAction, QPixmap

class MenuBar(QMenuBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        file_menu = self.addMenu("File")

        open_action = QAction("Open", self)
        save_action = QAction("Save", self)
        quit_action = QAction("Quit", self)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # optional, for clarity
        file_menu.addAction(quit_action)

        quit_action.triggered.connect(parent.close)
        open_action.triggered.connect(parent.open_image)
        #save_action.triggered.connect()


class ToolBar(QToolBar):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setFloatable(False)

        # --- Draw ---
        draw_action = QAction("Draw", self)
        #draw_action.triggered.connect(parent.start_draw_mode)
        self.addAction(draw_action)

        # --- Crop ---
        crop_action = QAction("Crop", self)
        #crop_action.triggered.connect(parent.start_crop_mode)
        self.addAction(crop_action)

        # --- Color Boost ---
        color_boost_action = QAction("Color Boost", self)
        #color_boost_action.triggered.connect(parent.color_boost)
        self.addAction(color_boost_action)

        # --- Black & White ---
        bw_action = QAction("Black & White", self)
        bw_action.triggered.connect(parent.black_and_white)
        self.addAction(bw_action)

        # --- Sharpen ---
        sharpen_action = QAction("Sharpen", self)
        #sharpen_action.triggered.connect(parent.sharpen)
        self.addAction(sharpen_action)

        # --- Box Blur ---
        box_blur_action = QAction("Box Blur", self)
        #box_blur_action.triggered.connect(parent.box_blur)
        self.addAction(box_blur_action)

        # --- Saturation ---
        saturation_action = QAction("Saturation", self)
        #saturation_action.triggered.connect(parent.adjust_saturation)
        self.addAction(saturation_action)

        # --- Brightness ---
        brightness_action = QAction("Brightness", self)
        #brightness_action.triggered.connect(parent.adjust_brightness)
        self.addAction(brightness_action)

        # --- Undo ---
        undo_action = QAction("Undo", self)
        #undo_action.triggered.connect(parent.undo_action)
        self.addAction(undo_action)

        # --- Redo ---
        redo_action = QAction("Redo", self)
        #redo_action.triggered.connect(parent.redo_action)
        self.addAction(redo_action)


class SideBar(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Sidebar info area"))
        # add more widgets later

