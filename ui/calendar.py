import os
import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidgetItem, QHBoxLayout, QListWidget
from PyQt5.QtCore import QTimer, Qt, QDateTime, QDate
from PyQt5.QtGui import QFont, QFontDatabase
from libs.CalendarWidget import CalendarWidget

from libs.ListItem import ListItem
from models.Event import Event


class CalendarPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        
        # Create a label with text "ตารางงาน"
        label = QLabel("ตารางงาน")
        label.setStyleSheet("color: white;background:transparent;")
        layout.addWidget(label)

        
        font_filename = "NotoSansThai-Regular.ttf"
        font_path = os.path.abspath(os.path.join("fonts", font_filename))
        font_id = QFontDatabase.addApplicationFont(font_path)         
        font = QFont("Noto Sans Thai",25)
        self.main_window = QWidget()
        self.main_window.setFont(font)
        self.layout = QVBoxLayout()
        
        label = QLabel("Hello, สวัสดี")
        
        # Set the font for the label
        font = QFont("Noto Sans Thai")

         # Create a QHBoxLayout for the calendar and event list
        calendar_event_layout = QHBoxLayout()

        # Create a calendar widget and add it to the QHBoxLayout
      
        # Create a list widget for events and set its size policy
        holidays = [
            Event(QDate(2023, 1, 1), "วันขึ้นปีใหม่", "ตรุษจีน"),
            Event(QDate(2023, 4, 13), "วันสงกรานต์", "วันหยุดราชการ"),
            Event(QDate(2023, 5, 1), "วันแรงงาน", "วันหยุดราชการ"),
            Event(QDate(2023, 7, 5), "วันพระราชสมภพ", "วันหยุดราชการ"),
            Event(QDate(2023, 7, 10), "วันรัฐธรรมนูญ", "วันหยุดราชการ"),
            # Add more holidays here
        ]
        self.calendar_widget = CalendarWidget()
       

        self.event_list_widget = QListWidget()

        for i, holiday in enumerate(holidays, start=1):
            item = QListWidgetItem(self.event_list_widget)
            item.setStyleSheet(" font-size: 14px;")
            #item.setSizeHint(ListItem(holiday).sizeHint())
            self.event_list_widget.setItemWidget(item, ListItem(holiday.date.toString("dd"),holiday.title,holiday.subtitle))
            self.event_list_widget.setFixedWidth(200)

        calendar_event_layout.addWidget(self.calendar_widget)
        calendar_event_layout.addWidget(self.event_list_widget)
        
        layout.addLayout(calendar_event_layout)


        # Create a label for the clock
        self.clock_label = QLabel()        
        self.clock_label.setStyleSheet("color: white; font-size: 36px;")
        #layout.addWidget(self.clock_label)

        self.setStyleSheet("color:white;background-color: rgba(50, 50, 100, 100);border-radius: 10px;")
        self.setLayout(layout)

        font_path = os.path.join("fonts", "digital-7.ttf")
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id != -1:
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QFont(font_family, 12)  # Adjust font size as needed
            self.clock_label.setFont(custom_font)

        # Update the clock every second
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_clock)
        self.timer.start(1000)  # 1000 milliseconds = 1 second
        self.update_clock()

    def update_clock(self):
        # Get the current date and time
        current_datetime = QDateTime.currentDateTime()

        # Format the time as a string
        current_time = current_datetime.toString("hh:mm:ss")

        # Update the clock label text
        self.clock_label.setText(current_time)
