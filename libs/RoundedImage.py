import os
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPixmap, QPainter, QBrush, QColor
from PyQt5.QtCore import Qt

class RoundedImage(QWidget):
    image_cache = {}  # Class attribute to cache QPixmap objects

    def __init__(self, image_path, rounded=5, parent=None):
        super(RoundedImage, self).__init__(parent)

        self.image_path = image_path
        self.rounded = rounded

        # Check if the QPixmap for the image_path is already cached
        if image_path in RoundedImage.image_cache:
            self.pixmap = RoundedImage.image_cache[image_path]
        else:
            self.pixmap = QPixmap(self.image_path)
            RoundedImage.image_cache[image_path] = self.pixmap  # Cache the QPixmap object

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignCenter)  # Set the alignment of the layout to center

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Draw the image in a rounded shape
        rect = self.rect()
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.pixmap.scaled(rect.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)))
        painter.drawRoundedRect(rect, self.rounded, self.rounded)

    def setAlignment(self, alignment):
            self.layout.setAlignment(alignment)
