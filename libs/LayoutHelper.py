import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget
from PyQt5.QtGui import QPixmap, QColor, QPalette, QFont, QFontDatabase
from PyQt5.QtCore import Qt

class LayoutHelper:
    def __init__(self, window, central_widget, image_path):
        self.window = window
        self.central_widget = central_widget
        self.image_path = image_path
        self.set_background_image()
        self.center_window()
        self.set_custom_font()

    def set_background_image(self):
        pixmap = QPixmap(self.image_path)
        scaled_pixmap = pixmap.scaled(self.window.size(), Qt.KeepAspectRatioByExpanding)

        background_label = QLabel(self.window)
        background_label.setPixmap(scaled_pixmap)
        background_label.setGeometry(0, 0, self.window.width(), self.window.height())
        background_label.lower()  # Make the background label be behind other widgets

    def center_window(self):
        # Center the window on the screen
        available_geometry = QApplication.desktop().availableGeometry(self.window)
        self.window.move(available_geometry.center() - self.window.rect().center())

    def set_custom_font(self):
        # Set the custom font for the application with size 25
        # Load the custom font from the 'fonts' folder
        font_path = os.path.abspath(os.path.join("fonts", "NotoSansThai-Regular.ttf"))
        
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]

        custom_font = QFont(font_family, 25)
        QApplication.setFont(custom_font)