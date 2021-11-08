from PyQt5 import QtWidgets


class Social(QtWidgets.QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout(self)

        self.status_line = QtWidgets.QLabel()
        layout.addWidget(self.status_line)

        self.canvas = QtWidgets.QListWidget()
        layout.addWidget(self.canvas)

        bottom_layout = QtWidgets.QHBoxLayout()

        self.input_textbox = QtWidgets.QLineEdit()
        bottom_layout.addWidget(self.input_textbox)

        self.send_button = QtWidgets.QPushButton('Send')
        bottom_layout.addWidget(self.send_button)

        layout.addLayout(bottom_layout)
    
        self.setFixedHeight(120)

    def add_message(self, message):

        self.canvas.addItem(message)
        self.canvas.scrollToBottom()
