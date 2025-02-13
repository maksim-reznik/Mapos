import sys
from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QLabel, QMainWindow
import requests
import os


class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi('untitled.ui', self)
        self.api_server = 'https://static-maps.yandex.ru/1.x/'
        self.map_zoom = 8
        self.delta = 0.1
        self.map_ll = [37.621601, 55.753460]
        self.map_l = 'map'
        self.theme = 'light'
        self.api = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
        self.pushButton.clicked.connect(self.search)
        self.pushButton_2.clicked.connect(self.set_map)
        # self.pushButton_3.clicked.connect(self.set_sputnik)
        self.pushButton_5.clicked.connect(self.change_theme)
        self.refresh_map()

    def set_map(self):
        self.map_l = 'map'
        self.refresh_map()

    def change_theme(self):
        self.theme = 'dark' if self.theme == 'light' else 'light'
        self.refresh_map()

    def search(self):
        pass

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_PageUp and self.map_zoom <= 20:
            self.map_zoom += 1
        if event.key() == Qt.Key.Key_PageDown and self.map_zoom > 0:
            self.map_zoom -= 1
        if event.key() == Qt.Key.Key_A and self.map_ll[0] > self.map_zoom / 1000:
            self.map_ll[0] -= self.map_zoom / 1000
        if event.key() == Qt.Key.Key_D and self.map_ll[0] < 90 - self.map_zoom / 1000:
            self.map_ll[0] += self.map_zoom / 1000
        if event.key() == Qt.Key.Key_S and self.map_ll[1] < 90 - self.map_zoom / 1000:
            self.map_ll[1] -= self.map_zoom / 1000
        if event.key() == Qt.Key.Key_W and self.map_ll[1] > self.map_zoom / 1000:
            self.map_ll[1] += self.map_zoom / 1000
        self.refresh_map()

    def refresh_map(self):
        map_params = {
            'll': ','.join(map(str, self.map_ll)),
            'l': self.map_l,
            'z': self.map_zoom,
            'theme': self.theme,
            'apikey': self.api
        }
        response = requests.get(self.api_server, params=map_params)
        if not response:
            print('Err')
            print(requests.status_codes, response.reason)
            sys.exit()
        pixmap = QPixmap()
        pixmap.loadFromData(response.content)
        self.label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('dark')
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
