import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QPushButton
import cv2
from PyQt5.QtCore import QUrl

class CameraListPopup(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera List")
        self.setGeometry(100, 100, 300, 200)

        self.camera_list = self.get_camera_list()

        self.layout = QVBoxLayout()

        self.label = QLabel("Select a camera:")
        self.layout.addWidget(self.label)

        self.radio_buttons = []
        for idx, camera_name in enumerate(self.camera_list):
            radio_button = QRadioButton(camera_name)
            self.layout.addWidget(radio_button)
            self.radio_buttons.append(radio_button)

        self.start_button = QPushButton("Start")
        self.start_button.clicked.connect(self.start_button_clicked)
        self.layout.addWidget(self.start_button)

        self.setLayout(self.layout)

    def get_camera_list(self):
        camera_list = []
        for i in range(10):  # Check for up to 10 cameras (you can adjust this as needed)
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                camera_name = f"Camera {i}"
                camera_list.append(camera_name)
                cap.release()
        return camera_list

    def start_button_clicked(self):
        selected_camera = None
        for idx, radio_button in enumerate(self.radio_buttons):
            if radio_button.isChecked():
                selected_camera = self.camera_list[idx]
                break

        if selected_camera:
            print(f"Selected camera: {selected_camera}")
            # Add your code to start speech recognition using the selected camera here

 
