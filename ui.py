from PyQt5 import QtCore, QtWidgets, QtGui

from social import Social


class TrackList(QtWidgets.QTableWidget):
    track_selected = QtCore.pyqtSignal(int, str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(3)
        self.setColumnWidth(0, 300)
        self.setColumnWidth(1, 400)
        self.setColumnWidth(2, 200)
        self.setHorizontalHeaderLabels(['Artist', 'Track', 'File'])
        self.verticalHeader().hide()

        self.setSelectionBehavior(1)
        self.itemDoubleClicked.connect(self.track_clicked)

    def track_clicked(self, item):
        row = self.row(item)
        id_item = self.item(row, 2)
        self.track_selected.emit(-1, id_item.data(0))

    def set_track_info(self, data):
        for i, (filename, row) in enumerate(data.items()):
            self.insertRow(i)
            for j, info in enumerate([row['artist'], row['title'], filename]):
                item = QtWidgets.QTableWidgetItem(info)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                self.setItem(i, j, item)

    def contextMenuEvent(self, event):

        row = self.row(self.itemAt(event.pos()))
        track_id = self.item(row, 2).data(0)

        menu = QtWidgets.QMenu(self)
        load_action_1 = menu.addAction('Load to Deck 1')
        load_action_2 = menu.addAction('Load to Deck 2')
        action = menu.exec_(event.globalPos())

        if action == load_action_1:
            self.track_selected.emit(0, track_id)
        elif action == load_action_2:
            self.track_selected.emit(1, track_id)


class Deck(QtWidgets.QWidget):
    play_pause = QtCore.pyqtSignal(bool, int)
    tempo_changed = QtCore.pyqtSignal(int, int)

    def __init__(self, deck, parent=None):

        super().__init__(parent)
        self.deck = deck

        main_layout = QtWidgets.QHBoxLayout(self)
        layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(layout)

        self.track_info = QtWidgets.QLabel()
        layout.addWidget(self.track_info)

        self.play_button = QtWidgets.QPushButton('Play')
        self.play_button.setCheckable(True)
        self.play_button.clicked.connect(self.play_button_clicked)
        layout.addWidget(self.play_button)

        self.tempo_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.tempo_slider.setMinimum(-255)
        self.tempo_slider.setMaximum(+255)
        self.tempo_slider.valueChanged.connect(self.tempo_change)
        layout.addWidget(self.tempo_slider)

        self.vu_meter = QtWidgets.QProgressBar()
        self.vu_meter.setOrientation(2)

        main_layout.addWidget(self.vu_meter)

    @QtCore.pyqtSlot()
    def play_button_clicked(self):
        if self.play_button.isChecked():
            self.play_pause.emit(True, self.deck)
        else:
            self.play_pause.emit(False, self.deck)

    @QtCore.pyqtSlot(int)
    def tempo_change(self, value):
        self.tempo_changed.emit(value, self.deck)


class Ui(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Remote Decks')

        self.shortcut_close = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+Q'), self)

        layout = QtWidgets.QVBoxLayout(self)

        self.top_layout = QtWidgets.QTabWidget()
        layout.addWidget(self.top_layout)

        bottom_layout = QtWidgets.QHBoxLayout()
        self.decks = [
                Deck(0),
                Deck(1)
                ]
        for deck in self.decks:
            bottom_layout.addWidget(deck)

        layout.addLayout(bottom_layout)

        self.cross_fader = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.cross_fader.setMinimum(-256)
        self.cross_fader.setMaximum(+256)
        layout.addWidget(self.cross_fader)

        self.social = Social()
        layout.addWidget(self.social)

    def add_track_list(self, name):

        track_list = TrackList()
        self.top_layout.addTab(track_list, name)
        index = self.top_layout.indexOf(track_list)

        return index, track_list
    
    def set_track_list(self, index, data):
        track_list = self.top_layout.widget(index)
        track_list.set_track_info(data)
