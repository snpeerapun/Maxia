import os
import sys
import sys
import threading
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QWidget,QDialog
from PyQt5.QtCore import Qt, pyqtSignal, pyqtSlot, QObject,QTimer
from PyQt5.QtGui import QPixmap, QColor, QPalette,QFontDatabase,QFont
 
#from libs.CategoryRecognizer import CategoryRecognizer
from libs.LayoutHelper import LayoutHelper
from libs.RoundedButton import RoundedButton
from libs.TextRecognizer import TextRecognizer
from libs.TextToSpeech import TextToSpeech
from ui.home import HomePage
from ui.musicplayer import MusicPlayerPage
from ui.calendar import CalendarPage
from ui.setting import SettingPage
from ui.youtube import YouTubePage
import threading
import speech_recognition as sr
from sys import platform
class PopupDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent, flags=Qt.WindowFlags(Qt.FramelessWindowHint))

        self.layout = QVBoxLayout()
        self.layout.addWidget(QPushButton("Close Popup", self, clicked=self.close))
    
        container = QWidget(self)
        container.setLayout(self.layout)

        self.setFixedSize(200, 200)
        #self.setCentralWidget(container)

    def exit_app(self):
        app = QApplication.instance()
        app.closeAllWindows()


class Worker(QObject):
    recognized = pyqtSignal(str,str)
    text_recognizer = TextRecognizer()
    text_recognizer.load_model('models/intent_model.pkl')
    def __init__(self):
        super().__init__()
        # Usage
       
 
    @pyqtSlot()
    def do_work(self):
        recognizer = sr.Recognizer()

        # Get the list of available microphones
        #microphone_list = sr.Microphone.list_microphone_names()

        # Display the list of microphone names (for troubleshooting)
        #print("Available microphones:", microphone_list)

        # Specify the index of the active microphone you want to use
        #active_microphone_index = 0  # Replace with the desired index of the active microphone

        # Initialize the microphone within a try-except block
        try:
            with sr.Microphone() as source:
                recognizer = sr.Recognizer()
                #category_recognizer = CategoryRecognizer()

                while True:
                    try:
                        audio = recognizer.listen(source)

                        recognized_text = recognizer.recognize_google(audio)                        
                        #category =  category_recognizer.get_most_similar_category(recognized_text)
                        recognized = self.text_recognizer.predict_intent(recognized_text)
                        print('you said:'+recognized_text)
                        TextToSpeech.speak("You said:"+recognized_text)
                        print('you mean:'+recognized)
                        TextToSpeech.speak('you mean:'+recognized)
                        self.recognized.emit(recognized_text,"category")
                    except sr.UnknownValueError:
                        print("Listening for speech...")
                    except Exception as e:
                        print(f"Error: {e}")
                        break  # Exit the loop if an error occurs

        except sr.RequestError as e:
            print(f"Error initializing microphone: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Listening for speech...")
        self.setGeometry(0, 0, 800, 480)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
 

        self.create_layout()
        if platform == "linux" or platform == "linux2":
            self.fullscreen = False  # Keep track of fullscreen state
            self.setWindowState(Qt.WindowFullScreen) 
        elif platform == "darwin":
            self.fullscreen = False 
        elif platform == "win32":
            self.fullscreen=False
            
        
         # Start in fullscreen

   
  
    def set_background_image(self, image_path):
        pixmap = QPixmap(image_path)
        scaled_pixmap = pixmap.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        background_label = QLabel(self)
        background_label.setPixmap(scaled_pixmap)
        background_label.setGeometry(0, 0, self.width(), self.height())
        background_label.lower()  # Make the background label be behind other widgets

    def create_layout(self):
        # Left section - menu buttons
        self.sidebar_widget = QWidget()
        self.sidebar_widget.setStyleSheet("color:white;background-color: rgba(50, 50, 100, 100);")        
        self.sidebar_layout = QVBoxLayout()
        self.sidebar_layout.setAlignment(Qt.AlignTop)
        self.sidebar_widget.setLayout(self.sidebar_layout)       
        self.sidebar_widget.setFixedWidth(80)

        self.menu_button_1 = RoundedButton("images/icons-home.png")
        self.menu_button_1.clicked.connect(lambda: self.change_page(HomePage()))
        self.menu_button_2 = RoundedButton("images/icons-schedule.png")
        self.menu_button_2.clicked.connect(lambda: self.change_page(CalendarPage()))
        self.menu_button_3 = RoundedButton("images/icons-music.png")
        self.menu_button_3.clicked.connect(lambda: self.change_page(MusicPlayerPage()))
        self.menu_button_4 = RoundedButton("images/icons-youtube.png")          
        self.menu_button_4.clicked.connect(lambda: self.change_page(YouTubePage()))
       
        self.menu_button_5 = RoundedButton("images/icons-setting.png")          
        self.menu_button_5.clicked.connect(lambda: self.change_page(SettingPage()))
        self.menu_button_6 = RoundedButton("images/icons-power-off.png")          
        self.menu_button_6.clicked.connect(lambda: self.close())
       

        self.sidebar_layout.addWidget(self.menu_button_1)
        self.sidebar_layout.addWidget(self.menu_button_2)
        self.sidebar_layout.addWidget(self.menu_button_3)
        self.sidebar_layout.addWidget(self.menu_button_4)      
        self.sidebar_layout.addWidget(self.menu_button_5)
        self.sidebar_layout.addWidget(self.menu_button_6)
       

        # Right section - pages
        self.right_widget = QVBoxLayout()

        # Main layout - left and right sections
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.sidebar_widget)
        main_layout.addLayout(self.right_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.central_widget.setLayout(main_layout)
        
        # Show initial page (Layout1)
        self.change_page(HomePage())
        self.start_task()
        # Apply the QGraphicsBlurEffect to the layout widget for frosted glass effect


     
    def handle_recognized(self, text,category):
        #popup = PopupDialog(self)
        #popup.exec_()
    
       
        if text=="music" :
            self.change_page(MusicPlayerPage()) 
        elif  text=="appoinment" :
            self.change_page(MusicPlayerPage()) 
        elif  text=="calendar" :
            self.change_page(CalendarPage())   

        self.setWindowTitle(text)
        #QTimer.singleShot(3000, popup.exit_app)

    def start_task(self):

        #self.text_label.setText("Listening for speech...")    
        self.worker_thread = threading.Thread(target=self.perform_task)
        self.worker_thread.daemon = True
        self.worker_thread.start()
        
    def perform_task(self):
        worker = Worker()
        worker.recognized.connect(self.handle_recognized)
        worker.do_work()

    def change_page(self, layout):
        # Clear the current layout
        for i in reversed(range(self.right_widget.count())):
            self.right_widget.itemAt(i).widget().setParent(None)

        # Add the new layout
        self.right_widget.addWidget(layout)
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.toggle_fullscreen()

    def toggle_fullscreen(self):
        if self.fullscreen:
            self.showNormal()  # Exit fullscreen
        else:
            self.showFullScreen()  # Enter fullscreen
        self.fullscreen = not self.fullscreen  # Toggle state

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    image_path = os.path.join("images", "bg2.png")
    layout_helper = LayoutHelper(window, window.central_widget, image_path)
    window.show()
    sys.exit(app.exec_())
