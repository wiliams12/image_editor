from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QMenuBar, QToolBar,
    QStatusBar, QLabel, QFrame, QFileDialog, QPushButton, QDialog, QCheckBox, QSlider, QSizePolicy
)
from PySide6.QtGui import QAction, QPixmap, QIcon
from PySide6.QtCore import Qt

from PIL import Image, ImageQt, ImageOps

from ui_bars import *

from image_label import ImageLabel

import numpy as np



class MainWindow(QMainWindow):
    def __init__(self, app, editor):
        super().__init__()
        self.app = app
        self.editor = editor
        self.setWindowTitle("Image Editor")
        self.setWindowIcon(QIcon("static\icon.png"))

        # --- Menu bar ---
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar)

        # --- Tool bar ---
        self.tool_bar = ToolBar(self)
        self.addToolBar(self.tool_bar)

        # --- Status bar ---
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # --- Central layout ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # --- Image display area ---
        self.image_label = ImageLabel(self)
        self.image_label.setFrameShape(QFrame.StyledPanel)
        self.image_label.setScaledContents(False)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        main_layout.addWidget(self.image_label)


        self.showMaximized()

    def open_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if not file_path:
            return

        # Let editor load the image (stores pixels internally)
        self.editor.load(file_path)

        # Ensure correct orientation for display
        image = Image.open(file_path)
        image = ImageOps.exif_transpose(image)
        self.editor.image = image  # update editor image (for consistency)

        # Update the display
        self.update_display()

        # Clear the button text if using button method
        if isinstance(self.image_label, QPushButton):
            self.image_label.deleteLater()
            self.image_label = QLabel()
            self.image_label.setAlignment(Qt.AlignCenter)
            self.centralWidget().layout().insertWidget(0, self.image_label)

        self.status_bar.showMessage(f"Opened: {file_path}")


    def update_display(self):
        """Update the QLabel with the current image in self.editor."""
        if self.editor.image is None:
            return  # nothing to display

        # Convert the editor image (Pillow Image or pixel data) to QPixmap
        qt_image = ImageQt.ImageQt(self.editor.show())  # editor.image must be a PIL Image
        pixmap = QPixmap.fromImage(qt_image)

        # Display it
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
        ))


    def ask_value_and_apply(self, func, min_val, max_val, default_val, title, with_channels=False):
        """
        Opens a popup with a slider to select a value.
        Optionally adds RGB checkboxes (for color boost).
        Calls update_img(func) with the chosen value (and channel if applicable).
        """
        dialog = QDialog(self)
        dialog.setWindowTitle(title)

        layout = QVBoxLayout(dialog)

        # --- Slider section ---
        label = QLabel(f"{title}: {default_val}")
        slider = QSlider(Qt.Horizontal)
        slider.setMinimum(min_val)
        slider.setMaximum(max_val)
        slider.setValue(default_val)

        layout.addWidget(label)
        layout.addWidget(slider)

        # --- RGB checkboxes (only for color boost) ---
        channel_checkboxes = []
        if with_channels:
            channel_layout = QHBoxLayout()
            for name in ["R", "G", "B"]:
                cb = QCheckBox(name)
                channel_layout.addWidget(cb)
                channel_checkboxes.append(cb)
            channel_checkboxes[0].setChecked(True)  # default: Red
            layout.addLayout(channel_layout)

        # --- Buttons ---
        apply_btn = QPushButton("Apply")
        cancel_btn = QPushButton("Cancel")
        layout.addWidget(apply_btn)
        layout.addWidget(cancel_btn)

        # --- Events ---
        slider.valueChanged.connect(lambda v: label.setText(f"{title}: {v}"))

        def on_apply():
            value = slider.value()

            if with_channels:
                for i, cb in enumerate(channel_checkboxes):
                    if cb.isChecked():
                        # pass both value and channel index
                        self.update_img(lambda: func(value, i))
                        break
            else:
                # normal single-argument filter
                self.update_img(lambda: func(value))

            dialog.accept()

        apply_btn.clicked.connect(on_apply)
        cancel_btn.clicked.connect(dialog.reject)

        dialog.exec()


    def update_img(self, func):
        self.editor.new_edit()
        func()
        self.update_display()

    def black_and_white(self):
        self.editor.black_and_white()

    def edge_enhancer(self):
        self.editor.edge_enhancer()

    def sharpen(self):
        self.editor.sharpen()

    def box_blur(self, size=3):
        self.editor.box_blur(size)

    def color_boost(self, amount=60, channel=0):
        self.editor.color_boost(amount, channel)

    def saturation(self, amount=60):
        self.editor.saturation(amount)

    def brightness(self, amount=60):
        self.editor.brightness(amount)

    def undo(self):
        self.editor.go_back()
        self.update_display()

    def redo(self):
        self.editor.go_forward()
        self.update_display()

    def save_img(self):
        if not self.editor.state or self.editor.state[self.editor.current] is None:
            self.status_bar.showMessage("No image to save.")
            return

        # Ask the user where to save
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Image As",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )

        if file_path:
            # Convert the current state's pixels to an image
            image = Image.fromarray(self.editor.state[self.editor.current].astype(np.uint8))
            image.save(file_path)
            self.status_bar.showMessage(f"Saved: {file_path}")
