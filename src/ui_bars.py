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
        draw_action.triggered.connect(lambda: parent.image_label.enable_draw(True))
        self.addAction(draw_action)

        # --- Crop ---
        crop_action = QAction("Crop", self)
        crop_action.triggered.connect(lambda: parent.image_label.enable_crop(True))
        self.addAction(crop_action)


        # --- Black & White ---
        bw_action = QAction("Black & White", self)
        bw_action.triggered.connect(lambda: parent.update_img(parent.black_and_white))
        self.addAction(bw_action)

        # --- Sharpen ---
        sharpen_action = QAction("Sharpen", self)
        sharpen_action.triggered.connect(lambda: parent.update_img(parent.sharpen))
        self.addAction(sharpen_action)


        #---- Edge enhancer
        edge_action = QAction("Edge Enhancer", self)
        edge_action.triggered.connect(lambda: parent.update_img(parent.edge_enhancer))
        self.addAction(edge_action)

        # --- Color Boost ---
        color_boost_action = QAction("Color Boost", self)
        color_boost_action.triggered.connect(lambda: parent.ask_value_and_apply(parent.color_boost, 0, 100, 50, "Color Boost Intensity", with_channels=True))
        self.addAction(color_boost_action)

        # --- Box Blur ---
        box_blur_action = QAction("Box Blur", self)
        box_blur_action.triggered.connect(lambda: parent.ask_value_and_apply(parent.box_blur, 1, 5, 3, "Box Blur Size"))
        self.addAction(box_blur_action)

        # --- Saturation ---
        saturation_action = QAction("Saturation", self)
        saturation_action.triggered.connect(lambda: parent.ask_value_and_apply(parent.saturation, 0, 100, 50, "Saturation"))
        self.addAction(saturation_action)

        # --- Brightness ---
        brightness_action = QAction("Brightness", self)
        brightness_action.triggered.connect(lambda: parent.ask_value_and_apply(parent.brightness, 0, 100, 50, "Brightness"))
        self.addAction(brightness_action)

        # --- Undo ---
        undo_action = QAction("Undo", self)
        undo_action.triggered.connect(parent.undo)
        self.addAction(undo_action)

        # --- Redo ---
        redo_action = QAction("Redo", self)
        redo_action.triggered.connect(parent.redo)
        self.addAction(redo_action)