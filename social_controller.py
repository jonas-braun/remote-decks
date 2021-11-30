import time

from PyQt5 import QtCore


class SocialController(QtCore.QObject):

    def __init__(self, controller, ui):

        super().__init__()

        self.controller = controller
        self.ui = ui

        self.social = self.ui.social

        self.status = {}

        self.greetings = set()

        self.social.input_textbox.returnPressed.connect(self.send)
        self.social.send_button.clicked.connect(self.send)

        self.syn_timer = QtCore.QTimer()
        self.syn_timer.setInterval(10000)
        self.syn_timer.timeout.connect(self.check_status)
        self.syn_timer.start()

    def update_status(self, timestamp, sender):

        if sender not in self.status:
            for greeting in self.greetings:
                self.controller.event_bus.send_data(time.time(), greeting)

        self.status[sender] = timestamp
        self.social.show_status(self.status)

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

        self.update_status(timestamp, sender)

    def receive_chat(self, timestamp, sender, message):
        self.social.add_message(sender + ' - ' + message[:256])

        self.update_status(timestamp, sender)

    @QtCore.pyqtSlot()
    def check_status(self):

        now = time.time()

        for sender, timestamp in self.status.copy().items():
            if now - timestamp > 30:
                del self.status[sender]
                self.social.show_status(self.status)

