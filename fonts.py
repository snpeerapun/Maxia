import os
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QFontDatabase, QFont

class FontExampleApp(QApplication):
    def __init__(self, args):
        super().__init__(args)

        font_filename = "NotoSansThai-Regular.ttf"
        font_path = os.path.abspath(os.path.join("fonts", font_filename))

        if os.path.exists(font_path):
            font_id = QFontDatabase.addApplicationFont(font_path)
            if font_id != -1:
                print("Font added successfully.")
            else:
                print("Failed to add font.")
        else:
            print("Font file not found:", font_path)

        self.main_window = QWidget()
        self.layout = QVBoxLayout()
        
        label = QLabel("Hello, สวัสดี")
        
        # Set the font for the label
        font = QFont("Noto Sans Thai")
        label.setFont(font)

        self.layout.addWidget(label)
        self.main_window.setLayout(self.layout)
        self.main_window.setWindowTitle("Font Example")
        self.main_window.show()

if __name__ == "__main__":
    app = FontExampleApp([])
    app.exec_()
