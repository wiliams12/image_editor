from PySide6.QtWidgets import QLabel, QRubberBand
from PySide6.QtCore import Qt, QRect, QPoint, QSize
from PySide6.QtGui import QColor

class ImageLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background-color: #333; color: white;")

        # --- Crop ---
        self.rubber_band = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()
        self.cropping_enabled = False

        # --- Drawing ---
        self.drawing_enabled = False
        self.draw_color = QColor(255, 0, 0)  # default red
        self.pen_size = 8
        self.pixel_set = set()
        self.last_point = None

        self.parent_window = parent  # MainWindow reference

    # --- Crop ---
    def enable_crop(self, enable=True):
        self.cropping_enabled = enable
        self.drawing_enabled = False
        if not enable:
            self.rubber_band.hide()

    # --- Draw ---
    def enable_draw(self, enable=True):
        self.drawing_enabled = enable
        self.cropping_enabled = False
        if enable:
            self.pixel_set.clear()
            self.last_point = None

    # --- Mouse events ---
    def mousePressEvent(self, event):
        if self.drawing_enabled and event.button() == Qt.LeftButton:
            self.pixel_set.clear()
            self.last_point = event.pos()
        elif self.cropping_enabled and event.button() == Qt.LeftButton:
            self.origin = event.pos()
            self.rubber_band.setGeometry(QRect(self.origin, QSize()))
            self.rubber_band.show()


    def mouseReleaseEvent(self, event):
        if self.drawing_enabled and event.button() == Qt.LeftButton:
            if self.pixel_set:
                self.parent_window.update_img(lambda: self.parent_window.editor.draw(self.pixel_set))
            self.enable_draw(False)
        elif self.cropping_enabled and event.button() == Qt.LeftButton:
            self._apply_crop(event)

    def mouseMoveEvent(self, event):
        if self.drawing_enabled and event.buttons() & Qt.LeftButton:
            if self.last_point is not None:
                self._record_line_pixels(self.last_point, event.pos())
            self.last_point = event.pos()
        elif self.cropping_enabled and self.rubber_band.isVisible():
            rect = QRect(self.origin, event.pos()).normalized()
            self.rubber_band.setGeometry(rect)

    # --- Helpers ---
    def _record_line_pixels(self, start_pos, end_pos):
        """Add pixels along a line between start_pos and end_pos (label coords)."""
        from math import ceil, sqrt

        # Bresenham-like approach for all pixels along the line
        x0, y0 = start_pos.x(), start_pos.y()
        x1, y1 = end_pos.x(), end_pos.y()

        dx = x1 - x0
        dy = y1 - y0
        distance = max(abs(dx), abs(dy))
        if distance == 0:
            self._record_pixel(end_pos)
            return

        for step in range(distance + 1):
            x = int(x0 + dx * step / distance)
            y = int(y0 + dy * step / distance)
            self._record_pixel(QPoint(x, y))

    def _record_pixel(self, pos):
        """Convert label coordinates to image coordinates and add all pixels in brush radius."""
        pixmap = self.pixmap()
        if not pixmap:
            return

        img_h, img_w = self.parent_window.editor.state[self.parent_window.editor.current].shape[:2]
        scaled_size = pixmap.size()
        x_ratio = img_w / scaled_size.width()
        y_ratio = img_h / scaled_size.height()
        x_offset = max((self.width() - scaled_size.width()) / 2, 0)
        y_offset = max((self.height() - scaled_size.height()) / 2, 0)

        x_center = int((pos.x() - x_offset) * x_ratio)
        y_center = int((pos.y() - y_offset) * y_ratio)

        if not (0 <= x_center < img_w and 0 <= y_center < img_h):
            return

        rgb = (self.draw_color.red(), self.draw_color.green(), self.draw_color.blue())

        radius = max(1, self.pen_size // 2)
        for dy in range(-radius, radius + 1):
            for dx in range(-radius, radius + 1):
                if dx*dx + dy*dy <= radius*radius:
                    x = x_center + dx
                    y = y_center + dy
                    if 0 <= x < img_w and 0 <= y < img_h:
                        self.pixel_set.add(((x, y), rgb))



    def _apply_crop(self, event):
        """Handle crop release logic."""
        self.rubber_band.hide()
        rect = self.rubber_band.geometry()
        pixmap = self.pixmap()
        if not pixmap:
            return

        img_h, img_w = self.parent_window.editor.state[self.parent_window.editor.current].shape[:2]
        scaled_size = pixmap.size()
        x_ratio = img_w / scaled_size.width()
        y_ratio = img_h / scaled_size.height()
        x_offset = max((self.width() - scaled_size.width()) / 2, 0)
        y_offset = max((self.height() - scaled_size.height()) / 2, 0)

        x1 = int((rect.x() - x_offset) * x_ratio)
        y1 = int((rect.y() - y_offset) * y_ratio)
        x2 = int((rect.right() - x_offset) * x_ratio)
        y2 = int((rect.bottom() - y_offset) * y_ratio)

        new_width, new_height = x2 - x1, y2 - y1
        if new_width > 0 and new_height > 0:
            self.parent_window.update_img(lambda: self.parent_window.editor.crop((new_width, new_height), (x1, y1)))

        self.enable_crop(False)
