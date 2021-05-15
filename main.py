#!/usr/bin/env python3

import sys
import json
import time
import asyncio
import datetime
import threading

from PyQt5 import QtCore, QtWidgets
from asyncqt import QEventLoop


class Ui(QtWidgets.QWidget):
    sendData = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Remote Decks')

        layout = QtWidgets.QVBoxLayout(self)

        self.play_button = QtWidgets.QPushButton('Play')
        self.play_button.setCheckable(True)
        # self.play_button.clicked.connect(self.button_clicked)
        layout.addWidget(self.play_button)

        self.tempo_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.tempo_slider.setMinimum(-8)
        self.tempo_slider.setMaximum(+8)
        layout.addWidget(self.tempo_slider)


class Engine(threading.Thread):

    def __init__(self):
        super().__init__()

        self.running = False

        self.start()

        while not self.running:
            time.sleep(.2)


    def run(self):

        from player import Player

        self.player_1 = Player()
        self.player_1.load_audio_file('test.wav')

        self.running = True

        while True:
            time.sleep(1)


    def play(self):

        self.player_1.play()


class Controller(QtCore.QObject):

    def __init__(self, engine):

        self.engine = engine

        self.ui = Ui()
        self.ui.show()

        self.engine.play()

    @QtCore.pyqtSlot(bool)
    def play_pause_clicked(self, value):

        print(value)


def main():
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)

    engine = Engine()

    controller = Controller(engine)
    
    with loop:

        loop.run_forever()
        




if __name__ == '__main__':
    main()
