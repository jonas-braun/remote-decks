import datetime

from PyQt5 import QtCore

from ui import Ui
from events import EventBus
from library import Library


class Controller(QtCore.QObject):

    def __init__(self, app, loop, engine):

        super().__init__()

        self.app = app
        self.loop = loop
        self.engine = engine

        self.event_bus = EventBus(loop, self)

        self.ui = Ui()
        self.ui.show()

        self.ui.shortcut_close.activated.connect(self.close_app)

        self.ui.decks[0].play_pause.connect(self.play_pause_clicked)
        self.ui.decks[1].play_pause.connect(self.play_pause_clicked)
        self.ui.decks[0].tempo_slider.valueChanged.connect(self.tempo_changed)

        self.library = Library()
        self.ui.track_list.track_selected.connect(self.load_track)
        self.ui.track_list.track_selected_to_deck.connect(self.load_track)
        self.load_track_list()

    def close_app(self):
        self.app.quit()


    @QtCore.pyqtSlot(bool, int)
    def play_pause_clicked(self, value, deck):

        if value is True:
            self.engine.play(deck)
            self.send_play()
        else:
            self.engine.pause(deck)

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

    def load_track(self, index, deck=None):

        if deck is None:
            deck = 0

        self.ui.decks[deck].track_info.setText('loading...')
        self.ui.decks[deck].repaint()
        track = self.library.get(index)
        self.engine.load_track(deck, track)
        self.ui.decks[deck].track_info.setText(track)


