from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QMenuBar, QToolBar,
    QStatusBar, QLabel, QFrame, QFileDialog, QPushButton
)
from PySide6.QtGui import QAction, QPixmap
from PySide6.QtCore import Qt

from PIL import Image, ImageQt, ImageOps

from ui_bars import *



class MainWindow(QMainWindow):
    def __init__(self, app, editor):
        super().__init__()
        self.app = app
        self.editor = editor
        self.setWindowTitle("Image Editor")

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
        self.image_label = QLabel("No image loaded")
        self.image_label.setFrameShape(QFrame.StyledPanel)
        self.image_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.image_label, 3)


        # --- Sidebar ---
        sidebar = SideBar()
        main_layout.addWidget(sidebar, 1)


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


    def black_and_white(self):
        self.editor.black_and_white()
        self.update_display()