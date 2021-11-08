import datetime
import time

from PyQt5 import QtCore

from ui import Ui
from events import EventBus
from library import Library
from social_controller import SocialController


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
        self.ui.decks[0].tempo_changed.connect(self.tempo_changed)
        self.ui.decks[1].tempo_changed.connect(self.tempo_changed)

        self.library = Library()
        self.ui.track_list.track_selected.connect(self.load_track)
        self.load_track_list()

        self.ui.cross_fader.valueChanged.connect(self.cross_fade)

        self.social_controller = SocialController(self, self.ui)

    def close_app(self):
        self.app.quit()


    @QtCore.pyqtSlot(bool, int)
    def play_pause_clicked(self, value, deck):

        if value is True:
            position = self.engine.players[deck].get_position()
            self.engine.play(deck)
            self.send_play(deck, position)
        else:
            self.engine.pause(deck)
            self.send_pause(deck)

        print(value)


    def send_play(self, deck, position):
        timestamp = time.time()
        self.event_bus.send_data(timestamp, f'PLAY {deck} {position}')

    def receive_play(self, timestamp, deck, offset):
        self.ui.decks[int(deck)].play_button.setChecked(True)

        self.engine.play(int(deck), offset, timestamp)

    def send_load(self, deck, track):
        timestamp = time.time()
        self.event_bus.send_data(timestamp, f'LOAD {deck} {track}')

    def receive_load(self, timestamp, deck, track):
        self.load_track(deck, name=track, send=False)

    def send_pause(self, deck):
        timestamp = time.time()
        self.event_bus.send_data(timestamp, f'PAUSE {deck}')

    def receive_pause(self, timestamp, deck):
        self.engine.pause(deck)
        self.ui.decks[deck].play_button.setChecked(False)

    def send_tempo_changed(self, deck, tempo):
        timestamp = time.time()
        self.event_bus.send_data(timestamp, f'TEMPO {deck} {tempo}')

    def receive_tempo(self, timestamp, deck, tempo):
        self.engine.change_tempo(deck, tempo, timestamp)
        self.ui.decks[deck].tempo_slider.blockSignals(True)
        self.ui.decks[deck].tempo_slider.setValue(int(tempo*256))
        self.ui.decks[deck].tempo_slider.blockSignals(False)

    def send_cross_fade(self, value):
        timestamp = time.time()
        self.event_bus.send_data(timestamp, f'CROSSFADE {value}')

    def receive_cross_fade(self, timestamp, value):
        self.cross_fade(value, send=False)
        self.ui.cross_fader.blockSignals(True)
        self.ui.cross_fader.setValue(value)
        self.ui.cross_fader.blockSignals(False)

    @QtCore.pyqtSlot(int, int)
    def tempo_changed(self, value, deck):
        self.engine.change_tempo(deck, value/256)
        self.send_tempo_changed(deck, value/256)


    def receive(self, timestamp, sender, msg):

        print('RECEIVED', timestamp, msg)
        print(msg)
        if msg.startswith('PLAY'):
            _, deck, offset = msg.split(' ')
            self.receive_play(timestamp, int(deck), float(offset))
        elif msg.startswith('LOAD'):
            _, deck, track = msg.split(' ', 2)
            self.receive_load(timestamp, int(deck), track)
        elif msg.startswith('PAUSE'):
            _, deck = msg.split(' ')
            self.receive_pause(timestamp, int(deck))
        elif msg.startswith('TEMPO'):
            _, deck, tempo = msg.split(' ')
            self.receive_tempo(timestamp, int(deck), float(tempo))
        elif msg.startswith('CROSSFADE'):
            _, value = msg.split(' ')
            self.receive_cross_fade(timestamp, int(value))
        elif msg.startswith('SOC'):
            _, value = msg.split(' ', 1)
            self.social_controller.receive(timestamp, sender, value)


    def load_track_list(self):
        self.ui.track_list.set_track_info(self.library.get_list())

    @QtCore.pyqtSlot(int, int)
    def load_track(self, deck=None, index=None, name=None, send=True):

        if deck < 0:
            deck = 0

        self.ui.decks[deck].track_info.setText('loading...')
        self.ui.decks[deck].repaint()

        if name:
            pass
        elif index is not None:
            name = self.library.get_name(index)
        else:
            return

        track = self.library.get(name)

        if send is True:
            self.send_load(deck, name)  # TODO load earlier

        self.engine.load_track(deck, track)
        self.ui.decks[deck].track_info.setText(name)

    @QtCore.pyqtSlot(int)
    def cross_fade(self, value, send=True):
        # "Transition" linear mode
        left_volume = min(1, 1 - value/256)
        right_volume = min(1, 1 + value/256)

        self.engine.players[0].volume = left_volume
        self.engine.players[1].volume = right_volume

        if send is True:
            self.send_cross_fade(value)
