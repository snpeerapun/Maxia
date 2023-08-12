import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QObject, Signal, Slot
import cv2
import numpy as np
import face_recognition
from PyQt5.QtGui import QImage, QPixmap
from libs.FaceRecognition import FaceRecognition

class Layout2(QWidget):
    def __init__(self):
        super().__init__()
        self.aspect_ratio = 16 / 9
        self.layout = QVBoxLayout()
        # Create a label with text "This is Layout 1"
        self.label = QLabel("หน้า 2")       
        self.label.setStyleSheet("color: white;")        
        self.setStyleSheet("color:white;background-color: rgba(50, 50, 100, 100);border-radius: 5px;") 
        self.video_label = QLabel(self)
        #self.video_label.setAlignment(Qt.AlignTop)
        available_width = self.width()
        new_height = int(available_width / self.aspect_ratio)
        self.video_label.setFixedSize(available_width, new_height)
        self.video_label.setStyleSheet("color:white;background-color: rgba(50, 50, 100, 100);border-radius: 5px;;")
        

        self.capture_label = QLabel(self)
        self.capture_label.setAlignment(Qt.AlignCenter)

        self.capture_button = QPushButton("Take Photo", self)
        self.capture_button.clicked.connect(self.take_photo)  # Modified connection
 
        self.layout.addWidget(self.video_label)
        self.layout.addWidget(self.capture_label)
        self.layout.addWidget(self.capture_button)
        self.setLayout(self.layout)

        self.face_recognition_thread = FaceRecognition()
        self.face_recognition_thread.capture_frame_signal.connect(self.update_video_label)
        self.face_recognition_thread.start()

        self.person_counter = 0
     
    def update_video_label(self, image):
        self.video_label.setPixmap(QPixmap.fromImage(image))   

    def take_photo(self):  # Renamed function to take_photo
        pixmap = self.video_label.pixmap()
        if pixmap:
            self.person_counter += 1
            file_name = f"person_{self.person_counter}.jpg"
            image = pixmap.toImage()

            face_locations = face_recognition.face_locations(self.qimage_to_np(image))
            if len(face_locations) > 0:
                top, right, bottom, left = face_locations[0]
                face_pixmap = pixmap.copy(left, top, right - left, bottom - top)

                face_qimage = face_pixmap.toImage()
                face_qimage.save(os.path.join("people", file_name))
                self.capture_label.setText(f"Face saved as {file_name}")
            else:
                self.capture_label.setText("No face found in the frame")

    def qimage_to_np(self, qimage):
        qimage = qimage.convertToFormat(QImage.Format_RGB888)
        width = qimage.width()
        height = qimage.height()
        ptr = qimage.bits()
        ptr.setsize(qimage.byteCount())
        return np.array(ptr).reshape(height, width, 3)
    