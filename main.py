#!/usr/bin/env python3

import sys
import json
import time
import asyncio
import datetime
import threading

from PyQt5 import QtCore, QtWidgets
from asyncqt import QEventLoop

from events import EventBus
from engine import Engine


class Ui(QtWidgets.QWidget):
    play_pause = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Remote Decks')

        layout = QtWidgets.QVBoxLayout(self)

        self.play_button = QtWidgets.QPushButton('Play')
        self.play_button.setCheckable(True)
        self.play_button.clicked.connect(self.play_button_clicked)
        layout.addWidget(self.play_button)

        self.tempo_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.tempo_slider.setMinimum(-255)
        self.tempo_slider.setMaximum(+255)
        layout.addWidget(self.tempo_slider)
        
    @QtCore.pyqtSlot()
    def play_button_clicked(self):
        if self.play_button.isChecked():
            self.play_pause.emit(True)
        else:
            self.play_pause.emit(False)


class Controller(QtCore.QObject):

    def __init__(self, loop, engine):

        super().__init__()

        self.loop = loop
        self.engine = engine

        self.event_bus = EventBus(loop, self)

        self.ui = Ui()
        self.ui.show()

        self.ui.play_pause.connect(self.play_pause_clicked)
        self.ui.tempo_slider.valueChanged.connect(self.tempo_changed)


    @QtCore.pyqtSlot(bool)
    def play_pause_clicked(self, value):

        if value is True:
            self.engine.play()
            self.send_play()
        else:
            self.engine.pause()

        print(value)


    def send_play(self):
        timestamp = datetime.datetime.now()
        self.event_bus.send_data(timestamp, 'PLAY')

    def receive_play(self, timestamp):
        self.ui.play_button.setChecked(True)

        offset = datetime.datetime.now().timestamp() - float(timestamp)
        print('OFFSET', offset)

        self.engine.play(offset)


    @QtCore.pyqtSlot(int)
    def tempo_changed(self, value):
        self.engine.change_tempo(value/256)



    def receive(self, timestamp, msg):

        print('RECEIVED', timestamp, msg)
        if msg == 'PLAY':
            self.receive_play(timestamp)



def main():
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)

    engine = Engine()

    controller = Controller(loop, engine)
    
    with loop:

        loop.run_forever()
        




if __name__ == '__main__':
    main()
