from PyQt5 import QtCore

from ui import Ui
from events import EventBus


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

