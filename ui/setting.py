import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QScrollArea, QListView, QAbstractItemView
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QStandardItemModel, QStandardItem
class SettingPage(QWidget):

    def __init__(self):
        super(SettingPage, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Create a QListView
        self.list_view = QListView()
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

        # Create a QStandardItemModel to populate the list view
        self.model = QStandardItemModel()
        self.list_view.setModel(self.model)
        self.setStyleSheet("color:white;background-color:  rgba(50, 50, 100, 100);border-radius: 5px;") 
        # Populate the list with items
        for i in range(1, 50):
            item = QStandardItem(f"Item {i}")
            self.model.appendRow(item)

        # Add the list view to a scroll area
        scroll_area = QScrollArea()
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.list_view)
      # Apply custom style to the scrollbar
        scroll_area.setStyleSheet('QScrollBar:vertical { border: 2px solid white; background: white; width: 10px;}'
                                  'QScrollBar::handle:vertical { background: darkgrey; min-height: 20px; }')

        layout.addWidget(scroll_area)
        self.setLayout(layout)

        # Perform item animations
        self.animate_items()

    def animate_items(self):
        for row in range(self.model.rowCount()):
            item_index = self.model.index(row, 0)
            item_widget = self.list_view.indexWidget(item_index)
            if item_widget:
                anim = QPropertyAnimation(item_widget, b"geometry", self)
                anim.setDuration(500)
                anim.setStartValue(item_widget.geometry().translated(0, 50))
                anim.setEndValue(item_widget.geometry())
                anim.setEasingCurve(QEasingCurve.OutBack)
                anim.start()