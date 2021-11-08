import time

from PyQt5 import QtCore


class SocialController(QtCore.QObject):

    def __init__(self, controller, ui):

        super().__init__()

        self.controller = controller
        self.ui = ui

        self.social = self.ui.social

        self.social.send_button.clicked.connect(self.send)

        self.syn_timer = QtCore.QTimer()
        self.syn_timer.setInterval(10000)
        self.syn_timer.timeout.connect(self.check_status)
        self.syn_timer.start()

    @QtCore.pyqtSlot()
    def send(self):

        timestamp = time.time()

        text = self.social.input_textbox.text()[:256]

        self.controller.event_bus.send_data(timestamp, f'SOC CHAT {text}')

        self.social.add_message(text[:256])

        self.social.input_textbox.setText('')


    def receive(self, timestamp, sender, msg):

        print('received')
        if msg.startswith('SYN'):
            self.receive_syn(timestamp, sender)
        elif msg.startswith('CHAT'):
            _, value = msg.split(' ', 1)
            self.receive_chat(timestamp, sender, value)
        
    def receive_syn(self, timestamp, sender):
        pass

    def receive_chat(self, timetamp, sender, message):
        self.social.add_message(sender + ' - ' + message[:256])

    @QtCore.pyqtSlot()
    def check_status(self):

        pass
