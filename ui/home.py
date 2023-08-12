from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel,QPushButton
class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.fullscreen=False
        # Create a label with text "This is Layout 1"
        label = QLabel("HomePage")       
        label.setStyleSheet("color: white;")        
        self.setStyleSheet("color:white;background-color: rgba(185, 185, 185, 0.22);border-radius: 10px;") 
        self.setLayout(layout)
        self.capture_button = QPushButton("FullScereen", self)
        self.capture_button.clicked.connect(self.toggle_fullscreen)  # Modified connection
 
        layout.addWidget(label)
        layout.addWidget(self.capture_button)
        self.setLayout(layout)
    def toggle_fullscreen(self):
        if self.fullscreen:
            self.showNormal()  # Exit fullscreen
        else:
            self.showFullScreen()  # Enter fullscreen
        self.fullscreen = not self.fullscreen  # Toggle state    