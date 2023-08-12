from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        # Create a label with text "This is Layout 1"
        label = QLabel("HomePage")       
        label.setStyleSheet("color: white;")        
        self.setStyleSheet("color:white;background-color: rgba(185, 185, 185, 0.22);border-radius: 10px;") 
        self.setLayout(layout)
     
        layout.addWidget(label)
        self.setLayout(layout)