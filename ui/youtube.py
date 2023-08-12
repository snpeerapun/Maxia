import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
 
from PyQt5.QtCore import QUrl

class YouTubePage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

         
        # Create a QLineEdit for search input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("ค้นหา Youtube ที่นี่...")

        # Create a QPushButton for video play
        play_button = QPushButton("เล่น Youtube")
        play_button.clicked.connect(self.play_youtube_video)

   
        layout.addWidget(self.search_input)
        layout.addWidget(play_button)
     
        self.setStyleSheet("color:white;background-color: rgba(50, 50, 100, 100); border-radius: 5px; padding: 20px;")
        self.setLayout(layout)

    def play_youtube_video(self):
        search_query = self.search_input.text()
        if search_query:
            url = f"https://www.youtube.com/results?search_query={search_query}"
            self.web_view.setUrl(url)
