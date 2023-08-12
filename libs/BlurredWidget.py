import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsBlurEffect  # This import remains the same


class BlurredWidget(QWidget):
    def __init__(self, parent=None):
        super(BlurredWidget, self).__init__(parent)

        self.setObjectName("BlurredWidget")
        self.setStyleSheet("#BlurredWidget { background-color: rgba(255, 255, 255, 150); }")

        layout = QVBoxLayout()
        self.label = QLabel("Blurred Widget", self)
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Apply the blur effect to the widget
        blur_effect = QGraphicsBlurEffect()
        blur_effect.setBlurRadius(10)
        self.setGraphicsEffect(blur_effect)
