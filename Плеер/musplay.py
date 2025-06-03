import os
import sys
import pygame
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QScrollArea
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

SONG_ENDED = pygame.USEREVENT + 1
directory = r'C:\Users\vladi\Music\Не желательно трогать'


def paths(direct):
    song_path = []
    for root, dirs, files in os.walk(direct):
        for file in files:
            if file.endswith('.mp3'):
                song_path.append(os.path.join(root, file))
    return song_path


def get_song_titles(siero):
    songs = []
    for filename in os.listdir(siero):
        if filename.endswith('.mp3'):
            songs.append(filename)
    return songs


files = paths(directory)
song_titles = get_song_titles(directory)


class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        pygame.mixer.init()
        pygame.init()
        self.playlist = files
        self.current_song = 0
        self.timez = 0

    def initUI(self):
        self.setWindowTitle('⠀')
        play_font = QFont('Arial', 10)
        x, y = 112, 23
        self.setWindowIcon(QIcon('svo.png'))

        lay0 = QHBoxLayout()
        lay1 = QVBoxLayout()
        lay2 = QHBoxLayout()
        lay3 = QHBoxLayout()
        lay4 = QHBoxLayout()

        self.play_button = QPushButton('▷')
        self.play_button.setFont(play_font)
        self.play_button.setFixedSize(x, y)
        self.pause_button = QPushButton('═')
        self.pause_button.setFixedSize(x, y)
        self.next_button = QPushButton('>>>')
        self.next_button.setFixedSize(x, y)
        self.prev_button = QPushButton('<<<')
        self.prev_button.setFixedSize(x, y)

        self.song_title = QLabel('Текущая песня: None', self)
        self.label = QLabel('Громкость: 100%', self)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setRange(0, 100)
        self.slider.setValue(100)

        self.playlist_label = QLabel('Список песен:\n' + '\n'.join(song_titles), self)
        self.playlist_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.playlist_label.setWordWrap(True)
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFixedSize(266,100)
        self.scroll_area.setWidget(self.playlist_label)

        self.play_button.clicked.connect(self.play_music)
        self.pause_button.clicked.connect(self.pause_music)
        self.pause_button.clicked.connect(self.change_icon)
        self.next_button.clicked.connect(self.next_song)
        self.prev_button.clicked.connect(self.prev_song)
        self.slider.valueChanged.connect(self.change_volume)

        lay0.addLayout(lay1)
        lay1.addLayout(lay2)
        lay1.addLayout(lay3)
        lay1.addLayout(lay4)

        lay0.addWidget(self.scroll_area)
        lay1.addWidget(self.label)
        lay1.addWidget(self.slider)
        lay2.addWidget(self.song_title)
        lay3.addWidget(self.play_button)
        lay3.addWidget(self.pause_button)
        lay4.addWidget(self.prev_button)
        lay4.addWidget(self.next_button)

        self.setLayout(lay0)
        self.show()

    def stop_music(self):
        if self.player:
            self.player.stop()
            print("Музыка остановлена.")

    def closeEvent(self, event):
        self.stop_music()
        event.accept()

    def play_music(self):
        if self.timez == 0:
            self.setWindowIcon(QIcon('svo1.png'))
        pygame.mixer.music.load(self.playlist[self.current_song])
        pygame.mixer.music.play()
        pygame.mixer.music.set_endevent(SONG_ENDED)
        current_song_name = song_titles[self.current_song].rsplit('.', 1)[0]
        self.song_title.setText(f'{current_song_name}')

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def next_song(self):
        self.current_song = (self.current_song + 1) % len(self.playlist)
        self.play_music()

    def prev_song(self):
        self.current_song = (self.current_song - 1) % len(self.playlist)
        self.play_music()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == SONG_ENDED:
                self.next_song()

    def change_volume(self, value):
        volume = value / 100
        pygame.mixer.music.set_volume(volume)
        self.label.setText(f'Громкость: {value}%')

    def create_playlist(self, song_titles):


        return self.scroll_area  # Возвращаем область прокрутки для дальнейшего использования

    def change_icon(self):
        if self.timez % 2 == 0:
            self.setWindowIcon(QIcon(r'C:\Users\vladi\PycharmProjects\pythonProject3\svo.png'))
            self.timez += 1
        elif self.timez % 2 == 1:
            self.setWindowIcon(QIcon(r'C:\Users\vladi\PycharmProjects\pythonProject3\svo1.png'))
            self.timez += 1

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MusicPlayer()
    app.setStyle('Windows')
    while True:
        player.handle_events()
        app.processEvents()
    sys.exit(app.exec_())