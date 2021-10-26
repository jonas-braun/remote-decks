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


class TrackList(QtWidgets.QTableWidget):
    track_selected = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(2)
        self.setHorizontalHeaderLabels(['Artist', 'Track'])
        self.verticalHeader().hide()

        self.setSelectionBehavior(1)
        self.itemDoubleClicked.connect(self.track_clicked)

    def track_clicked(self, item):
        row = self.row(item)
        for i in range(2):
            item = self.item(row, i)
            item.setSelected(True)
        self.track_selected.emit(row)

    def set_track_info(self, data):
        for i, row in enumerate(data):
            self.insertRow(i)
            for j, info in enumerate(row):
                item = QtWidgets.QTableWidgetItem(info)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                self.setItem(i, j, item)


class Ui(QtWidgets.QWidget):
    play_pause = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Remote Decks')

        layout = QtWidgets.QVBoxLayout(self)

        self.track_list = TrackList()
        layout.addWidget(self.track_list)

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

        self.ui.track_list.track_selected.connect(self.load_track)
        self.load_track_list()


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


    def load_track_list(self):
        self.ui.track_list.set_track_info([['Demo', '1'], ['Demo', '2']])

    def load_track(self, index):
        print('Selected', index)
        pass




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
