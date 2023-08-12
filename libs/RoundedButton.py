import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtGui import QPainter, QColor, QBrush, QIcon, QPixmap
from PyQt5.QtCore import Qt

class RoundedButton(QPushButton):
    def __init__(self, icon_path, icon_size=40, transparent=False, parent=None):
        super(RoundedButton, self).__init__( parent)
        self.icon_size = 40  # Set the desired icon size (adjust as needed)
        pixmap = QPixmap(icon_path).scaled(icon_size, icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setIcon(QIcon(pixmap))
        self.setIconSize(pixmap.size())
        #self.setFixedSize(icon_size + 20, icon_size + 20)  # 
        #self.setIcon(QIcon("images/icon_home.png"))
        self.setFixedSize(60, 60)  # Set the button size (adjust as needed)
        self.default_color = QColor(74, 144, 226)  # Default color of the button
        self.pressed_color = QColor(37, 78, 119)   # Color when the button is pressed
        self.current_color = self.default_color
        # Set stylesheet for the pressed background color
        if transparent :
            self.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 15px;
                    padding:5px;                     
                    margin-bottom:7px;     
                    background-color: transparent;          
                }
                QPushButton:pressed {
                    background-color: transparent;
                
                }
            """)
        else:
           self.setStyleSheet("""
                QPushButton {
                    border: none;
                    border-radius: 15px;
                    padding:5px;                     
                    margin-bottom:7px;               
                }
                QPushButton:pressed {
                    background-color: transparent;
                
                }
            """)
    def setImage(self,image_path):
        self.image_path = image_path           
        pixmap = QPixmap(self.image_path).scaled(self.icon_size, self.icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setIcon(QIcon(pixmap))