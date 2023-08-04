import sys
import cv2
import face_recognition
import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QApplication, QDesktopWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt, QTimer
import datetime

class ShowVideo(QtCore.QObject):
    camera_port = 0
    camera = cv2.VideoCapture(camera_port)
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    VideoSignal = QtCore.pyqtSignal(QtGui.QImage)
    Stopped = QtCore.pyqtSignal()

    def startVideo(self):
        while True:
            ret, image = self.camera.read()

            if not ret:
                break

            faces = self.face_cascade.detectMultiScale(image, 1.3, 5)
            date = datetime.datetime.now()
            cv2.putText(image, str(date), (370, 470), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

            cv2.putText(image, "By FALCON TUNISIA", (15, 470), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1, cv2.LINE_AA)
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 255, 255), 5)

            color_swapped_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, _ = color_swapped_image.shape
            qt_image = QtGui.QImage(color_swapped_image.data, width, height, color_swapped_image.strides[0],
                                    QtGui.QImage.Format_RGB888)
            self.VideoSignal.emit(qt_image)

        self.Stopped.emit()

    def stopVideo(self):
        self.camera.release()


class FaceRecognitionApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

        self.thread = QtCore.QThread()
        self.vid = ShowVideo()
        self.vid.moveToThread(self.thread)
        self.thread.started.connect(self.vid.startVideo)
        self.vid.VideoSignal.connect(self.update_label)
        self.vid.Stopped.connect(self.thread.quit)
        self.thread.finished.connect(self.vid.stopVideo)
        self.thread.start()

    @QtCore.pyqtSlot(QtGui.QImage)
    def update_label(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def closeEvent(self, event):
        self.vid.stopVideo()
        self.thread.quit()
        self.thread.wait()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceRecognitionApp()

    # Set the window size to 800x640
    window.resize(800, 640)

    # Center the window on the screen
    window_rect = window.geometry()
    center_point = QDesktopWidget().availableGeometry().center()
    window_rect.moveCenter(center_point)
    window.move(window_rect.topLeft())

    window.setWindowTitle("Face Recognition App")
    window.show()
    sys.exit(app.exec_())
