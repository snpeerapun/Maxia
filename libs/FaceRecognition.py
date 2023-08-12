import sys
import os
import cv2
import face_recognition
 
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal, pyqtSlot

import numpy as np

class FaceRecognition(QThread):
    capture_frame_signal = Signal(QImage)

    def __init__(self):
        super().__init__()
        self.video_capture = cv2.VideoCapture(0)
        self.known_face_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        people_folder = 'people'
        if os.path.exists(people_folder) and os.path.isdir(people_folder):
            for file_name in os.listdir(people_folder):
                image = face_recognition.load_image_file(os.path.join(people_folder, file_name))
                face_encodings = face_recognition.face_encodings(image)

                if len(face_encodings) > 0:
                    face_encoding = face_encodings[0]
                    self.known_face_encodings.append(face_encoding)
                    self.known_face_names.append(os.path.splitext(file_name)[0])
                else:
                    print(f"No face found in {file_name}")

    def run(self):
        while True:
            ret, frame = self.video_capture.read()
            if not ret:
                break

            face_locations = face_recognition.face_locations(frame)
            face_encodings = face_recognition.face_encodings(frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = self.known_face_names[first_match_index]

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left , bottom + 12), cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            convert_to_qt_format = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_qt_format.scaled(640, 480, Qt.KeepAspectRatio)
            self.capture_frame_signal.emit(p)

        self.video_capture.release()