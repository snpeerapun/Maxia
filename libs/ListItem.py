import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPainter, QBrush

class RoundedLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setText(text)
        self.setStyleSheet("font-size: 15px;font-weight:bold")
        self.setAlignment(Qt.AlignCenter)
      
class ListItem(QWidget):
    def __init__(self, day, title, subtitle):
        super().__init__()
 
        # Create the QHBoxLayout
        h_layout = QHBoxLayout()

        # Create the image label
        image_label = RoundedLabel(day)
        image_label.setFixedWidth(50)
          # Replace with the path to your image
        h_layout.addWidget(image_label)

        # Create the QVBoxLayout
        v_layout = QVBoxLayout()

        # Create the title label
        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 13px; background:transparent")
        v_layout.addWidget(title_label)

        # Create the subtitle label
        subtitle_label = QLabel(subtitle)
        subtitle_label.setStyleSheet("font-size: 13px; color: gray;background:transparent")
        v_layout.addWidget(subtitle_label)

        # Add the QVBoxLayout to the QHBoxLayout
        h_layout.addLayout(v_layout)

        # Set the main window's layout
        self.setLayout(h_layout)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        radius = 10.0  # Adjust this value to control the roundness of the corners
        painter.setPen(Qt.NoPen)
       
        rect = self.rect()
        painter.drawRoundedRect(rect, radius, radius)

        super().paintEvent(event)
