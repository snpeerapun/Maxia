import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QIcon, QPixmap
class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        icon_size = QSize(50, 50)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.setStyleSheet("color:white;background-color: rgba(50, 50, 100, 0);border-radius: 10px;") 
        # Create the header with navigation buttons, month/year label, and weekday labels
        header_layout = QGridLayout()
        self.prev_button = QPushButton()

        font_path = os.path.join("images", "icons-back.png")      
        self.prev_button.setIcon(QIcon(font_path))
        self.prev_button.setIconSize(icon_size)
        #self.prev_button.setStyleSheet("background-color: rgba(50, 50, 100, 80);border-radius: 15px;")
        self.prev_button.clicked.connect(self.show_previous_month)
        header_layout.addWidget(self.prev_button, 0, 0)
 
        self.month_year_label = QLabel()
        self.month_year_label.setAlignment(Qt.AlignCenter)
        header_layout.addWidget(self.month_year_label, 0, 1, 1, 5)

        self.next_button = QPushButton()
        font_path = os.path.join("images", "icons-next.png")
        self.next_button.setIcon(QIcon(font_path))
        self.next_button.setIconSize(icon_size)
        #self.next_button.setStyleSheet("background-color: rgba(50, 50, 100, 80);border-radius: 15px;")
        self.next_button.clicked.connect(self.show_next_month)
        header_layout.addWidget(self.next_button, 0, 6)
       
        # Create weekday labels
        weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for col, weekday in enumerate(weekdays):
            weekday_label = QLabel(weekday)   
            weekday_label.setStyleSheet("font-size: 13px;font-weight:bold;")     
            weekday_label.setFixedHeight(50)   
               
            weekday_label.setAlignment(Qt.AlignCenter)
            header_layout.addWidget(weekday_label, 1, col)

        # Create a grid layout to arrange the days of the month
        self.grid_layout = QGridLayout()
        self.days_labels = []

        # Add the header and grid layout to the main layout
        layout.addLayout(header_layout)
        layout.addLayout(self.grid_layout)

        # Set the current date to today
        self.selected_date = QDate.currentDate()
        self.update_calendar()

    def update_calendar(self):
        # Clear the existing day labels
        for day_label in self.days_labels:
            day_label.deleteLater()

        # Update the header with the month and year name
        self.month_year_label.setText(self.selected_date.toString("MMMM yyyy"))

        # Get the first day of the month and the number of days in the month
        first_day_of_month = self.selected_date.addDays(-self.selected_date.day() + 1)
        days_in_month = self.selected_date.daysInMonth()

        # Get the day of the week for the first day of the month
        day_of_week = first_day_of_month.dayOfWeek()

        # Create labels for each day of the month
        self.days_labels = []
        for i in range(42):  # 6 rows of 7 days
            day_label = QLabel()
            day_label.setAlignment(Qt.AlignCenter)
            #day_label.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
            self.days_labels.append(day_label)

        # Add the day labels to the grid layout
        row = 2  # Start from row 2 to leave space for the header
        col = day_of_week - 1
        for day_label in self.days_labels:
            if col == 7:
                col = 0
                row += 1
            if row > 2 and (row - 2) * 7 + col + 1 > days_in_month:
                break
            self.grid_layout.addWidget(day_label, row, col)
            col += 1

        # Update the day labels with the days of the month
        day = 1
        for day_label in self.days_labels:
            if day <= days_in_month:
                day_label.setText(str(day))
                if self.selected_date == QDate.currentDate() and day == QDate.currentDate().day():
                    day_label.setStyleSheet("border: 2px solid red; border-radius: 15px;")
                else:
                    day_label.setStyleSheet("border: none;")
            else:
                day_label.setText("")
            day += 1

    def show_previous_month(self):
        self.selected_date = self.selected_date.addMonths(-1)
        self.update_calendar()

    def show_next_month(self):
        self.selected_date = self.selected_date.addMonths(1)
        self.update_calendar()
