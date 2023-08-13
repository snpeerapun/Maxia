import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

app = QApplication([])

 
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

app.exec_()

 