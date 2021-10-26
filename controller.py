import datetime

from PyQt5 import QtCore

from ui import Ui
from events import EventBus
from library import Library


class Controller(QtCore.QObject):

    def __init__(self, loop, engine):

        super().__init__()

        self.loop = loop
        self.engine = engine

        self.event_bus = EventBus(loop, self)

        self.ui = Ui()
        self.ui.show()

        self.ui.decks[0].play_pause.connect(self.play_pause_clicked)
        self.ui.decks[0].tempo_slider.valueChanged.connect(self.tempo_changed)

        self.library = Library()
        self.ui.track_list.track_selected.connect(self.load_track)
        self.load_track_list()


    @QtCore.pyqtSlot(bool)
    def play_pause_clicked(self, value):

        if value is True:
            self.engine.play(0)
            self.send_play()
        else:
            self.engine.pause(0)

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
        self.ui.track_list.set_track_info(self.library.get_list())

    def load_track(self, index):
        track = self.library.get(index)
        self.engine.load_track(0, track)
        self.ui.decks[0].track_info.setText(track)


