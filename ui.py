from PyQt5 import QtCore, QtWidgets


class TrackList(QtWidgets.QTableWidget):
    track_selected = QtCore.pyqtSignal(int)
    track_selected_to_deck = QtCore.pyqtSignal(int, int)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setColumnCount(2)
        self.setColumnWidth(0, 600)
        self.setHorizontalHeaderLabels(['Artist', 'Track'])
        self.verticalHeader().hide()

        self.setSelectionBehavior(1)
        self.itemDoubleClicked.connect(self.track_clicked)

    def track_clicked(self, item):
        row = self.row(item)
        self.track_selected.emit(row)

    def set_track_info(self, data):
        for i, row in enumerate(data):
            self.insertRow(i)
            for j, info in enumerate(row):
                item = QtWidgets.QTableWidgetItem(info)
                item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable)
                self.setItem(i, j, item)

    def contextMenuEvent(self, event):

        row = self.row(self.itemAt(event.pos()))

        menu = QtWidgets.QMenu(self)
        load_action_1 = menu.addAction('Load to Deck 1')
        load_action_2 = menu.addAction('Load to Deck 2')
        action = menu.exec_(event.globalPos())

        if action == load_action_1:
            self.track_selected_to_deck.emit(row, 0)
        elif action == load_action_2:
            self.track_selected_to_deck.emit(row, 1)


class Deck(QtWidgets.QWidget):
    play_pause = QtCore.pyqtSignal(bool, int)

    def __init__(self, deck, parent=None):

        super().__init__(parent)
        self.deck = deck

        layout = QtWidgets.QVBoxLayout(self)

        self.track_info = QtWidgets.QLabel()
        layout.addWidget(self.track_info)

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
            self.play_pause.emit(True, self.deck)
        else:
            self.play_pause.emit(False, self.deck)


class Ui(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle('Remote Decks')

        layout = QtWidgets.QVBoxLayout(self)

        self.track_list = TrackList()
        layout.addWidget(self.track_list)

        bottom_layout = QtWidgets.QHBoxLayout()
        self.decks = [
                Deck(0),
                Deck(1)
                ]
        for deck in self.decks:
            bottom_layout.addWidget(deck)

        layout.addLayout(bottom_layout)

