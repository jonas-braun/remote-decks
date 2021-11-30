import os
from functools import partial

from PyQt5 import QtCore

from library import Library
from storage import GoogleStorage


class LibraryController(QtCore.QObject):

    def __init__(self, controller, ui):

        super().__init__()

        self.controller = controller
        self.ui = ui

        self.libraries = {}
        folders = os.getenv('RD_LIBRARY')
        for folder in folders.split(':'):

            new_library = Library(folder)

            self.libraries[new_library.name] = new_library

            self.load_track_list(new_library)

        if os.getenv('RD_STORAGE_GOOGLE_BUCKET'):
            # host mode
            self.storage = GoogleStorage()
            assert self.storage.initialized
            
            bucket = os.getenv('RD_STORAGE_GOOGLE_BUCKET')
            token = self.storage.token
            self.controller.social_controller.greetings.add(f'LIBRARY {bucket} {token}')

    def receive(self, timetamp, sender, value):
        bucket, token = value.split(' ')

        if bucket not in self.remote_
        # TODO bucket + folder + token
        # TODO receive_load_track

    def load_track_list(self, library):
        index, track_list = self.ui.add_track_list(library.name)
        callback = partial(self.load_track, library_name=library.name)
        track_list.track_selected.connect(callback)

        self.ui.set_track_list(index, library.get_list())

    @QtCore.pyqtSlot(int, str)
    def load_track(self, deck=-1, name=None, library_name=None, send=True):

        if deck < 0:
            deck = 0

        self.ui.decks[deck].track_info.setText('loading...')
        self.ui.decks[deck].repaint()

        if not library_name:
            raise NotImplementedError

        if name:
            pass
        else:
            return

        track = self.libraries[library_name].get(name)

        if send is True:
            self.controller.send_load(deck, name)  # TODO load earlier

        self.controller.engine.load_track(deck, track)
        self.ui.decks[deck].track_info.setText(name)
