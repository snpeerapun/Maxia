import os
import sys
import threading
import eyed3
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSlider, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, QTimer
import tempfile
from PyQt5.QtWidgets import QGraphicsBlurEffect, QGraphicsDropShadowEffect

from libs.RoundedButton import RoundedButton
from models.music import Music
class MusicPlayerPage(QWidget):
    def __init__(self):
        super().__init__()

        self.music_folder = "music"
        self.music_files = []
        self.current_index = 0
        self.isPlay=False
        self.album_cover_label = QLabel()
        self.music_name_label = QLabel()
        self.music_name_label.setAlignment(Qt.AlignCenter)
        self.music_name_label.setFixedHeight(50)
        self.music_name_label.setStyleSheet("color:white;background-color:transparent;font-size:30px;")

        self.artist_label = QLabel()
        self.artist_label.setAlignment(Qt.AlignCenter)
      
        self.artist_label.setStyleSheet("color:white;background-color:transparent;font-size:15px;")
        
        self.playtime_label = QLabel("0.00")
        self.total_music_length_label = QLabel("0.00")
        self.playtime_label.setStyleSheet("color:white;background-color:transparent;font-size:9px")
        self.total_music_length_label.setStyleSheet("color:white;background-color:transparent;font-size:9px")

 
        self.random_button = RoundedButton(os.path.join("images", "icons-random.png"),40,True)
        self.back_button = RoundedButton(os.path.join("images", "icons-rewind.png"),40,True)
        self.play_button = RoundedButton(os.path.join("images", "icons-play.png"),40,True)        
        self.next_button = RoundedButton(os.path.join("images", "icons-forward.png"),40,True)
        self.favorite_button = RoundedButton(os.path.join("images", "icons-favorite"),40,True)

        self.seek_slider = QSlider(Qt.Horizontal, self)
        self.seek_slider.setStyleSheet("color:white;background-color:transparent;")
        self.seek_slider.setFixedWidth(350)
        self.seek_slider.setMinimum(0)
        self.seek_slider.setMaximum(10000)
        self.seek_slider.setValue(0)
        self.seek_slider.setSingleStep(1)
        self.seek_slider.sliderMoved.connect(self.set_position)
        self.seek_slider.sliderReleased.connect(self.seek_to_position)

        self.update_slider_timer = QTimer(self)
        self.update_slider_timer.timeout.connect(self.update_slider)
        self.update_slider_timer.start(100)  # Update the slider every 100 milliseconds

        self.random_button.clicked.connect(self.play_or_pause)
        self.back_button.clicked.connect(self.play_previous)
        self.play_button.clicked.connect(self.play_or_pause)        
        self.next_button.clicked.connect(self.play_next)
        self.favorite_button.clicked.connect(self.play_next)
        
        # Player layout
        player_layout = QVBoxLayout()
        player_layout.setAlignment(Qt.AlignCenter)
        player_layout.addWidget(self.album_cover_label, 1, Qt.AlignCenter)
        player_layout.addWidget(self.music_name_label, Qt.AlignCenter)
        player_layout.addWidget(self.artist_label, Qt.AlignCenter)
      
         # seekerbar layout
        seekbar_layout = QHBoxLayout()
        seekbar_layout.addWidget(self.playtime_label, Qt.AlignLeft)
        seekbar_layout.addWidget(self.seek_slider)
        seekbar_layout.addWidget(self.total_music_length_label, Qt.AlignRight)
        player_layout.addLayout(seekbar_layout)
    
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.random_button)
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.play_button)       
        button_layout.addWidget(self.next_button)
        button_layout.addWidget(self.favorite_button)
        player_layout.addLayout(button_layout)

        # Playlist layout
        self.playlist_widget = QListWidget()
        self.playlist_widget.setFixedWidth(220)
        #self.playlist_widget.setFont(font.setPointSize(10))
        self.playlist_widget.currentRowChanged.connect(self.playlist_item_changed)
        self.playlist_widget.setStyleSheet("color:white;background-color: rgba(50, 50, 100, 100);border-radius: 10px;font-size:13px")

        self.cover_widget = QWidget()        
        self.cover_widget.setStyleSheet("color:white;background-color: rgba(50, 50, 100, 100);border-radius: 10px;")
        self.cover_widget.setLayout(player_layout)
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.cover_widget)  # Player layout takes 1/3 of the width
        main_layout.addWidget(self.playlist_widget)  # Playlist layout takes 2/3 of the width
        self.setLayout(main_layout)
        pygame.init()
        #self.setStyleSheet("color:white;background-color: rgba(50, 50, 100, 100);border-radius: 10px;")
        self.load_music_files()
        self.update_ui()
        self.play()
    def load_music_files(self):
        self.music_files = [os.path.join(self.music_folder, f) for f in os.listdir(self.music_folder) if f.endswith(".mp3")]
        self.playlist_widget.clear()
        for music_file in self.music_files:
            music = Music(music_file)
            item = QListWidgetItem(os.path.splitext(os.path.basename(music_file))[0])  # Display file name without extension
            self.playlist_widget.addItem(item)
            item.setData(Qt.UserRole, music) 
    def update_ui(self):
        if self.music_files and 0 <= self.current_index < len(self.music_files):
            music = self.playlist_widget.item(self.current_index).data(Qt.UserRole)

             # Display artist name or "Unknown Artist"
            title = music.title if music.title else os.path.splitext(os.path.basename(music.file_path))[0]
            self.music_name_label.setText(title)            
           
            # Display artist name or "Unknown Artist"
            artist_name = music.artist if music.artist else "Unknown Artist"
            self.artist_label.setText(artist_name)

            # Read album cover and display it
            pixmap = QPixmap(music.album_cover_path)
            self.album_cover_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))

            # Update the total music length label
            total_length = music.duration
            minutes, seconds = divmod(int(total_length), 60)
            self.total_music_length_label.setText(f"{minutes:02d}:{seconds:02d}")

        else:
            self.music_name_label.setText("No music files found.")
            self.artist_label.setText("Unknown Artist")
            default_album_cover = os.path.join("images", "album_cover.jpg")
            pixmap = QPixmap(default_album_cover)
            self.album_cover_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            self.total_music_length_label.setText("00:00")
    def update_slider(self):
        if pygame.mixer.music.get_busy():
            position = pygame.mixer.music.get_pos() / 1000  # Convert milliseconds to seconds
            self.seek_slider.setValue(position)
          
            # Update the playtime label
            minutes, seconds = divmod(int(position), 60)
            self.playtime_label.setText(f"{minutes:02d}:{seconds:02d}")

    def play_previous(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_ui()
            self.play()

    def play_or_pause(self):
        if self.isPlay==False :
            self.play()
        else:
            self.pause()

    def play(self):
        if self.music_files and 0 <= self.current_index < len(self.music_files):
            music = self.playlist_widget.item(self.current_index).data(Qt.UserRole)
            pygame.mixer.music.load(music.file_path)
            pygame.mixer.music.play()
            #self.play_button.setText("Pause")
            self.isPlay=True
            self.play_button.setImage(os.path.join("images", "icons-pause.png"))
    def pause(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.isPlay=False
            self.play_button.setImage(os.path.join("images", "icons-play.png"))

    def play_next(self):
        if self.current_index < len(self.music_files) - 1:
            self.current_index += 1
            self.update_ui()
            self.play()

    def stop(self):
        pygame.mixer.music.stop()
        self.seek_slider.setValue(0)
        self.play_button.setImage(os.path.join("images", "icons-play.png"))

    def set_position(self, position):
        # Set the audio playback position based on the slider value
        pygame.mixer.music.set_pos(position / 1000)

    def seek_to_position(self):
        position = self.seek_slider.value()
        pygame.mixer.music.set_pos(position)

    def playlist_item_changed(self, index):
        self.current_index = index
        self.update_ui()
        self.play()