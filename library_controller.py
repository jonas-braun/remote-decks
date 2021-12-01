import os
from functools import partial

from PyQt5 import QtCore

from library import Library, RemoteLibrary
from storage import GoogleStorage


class LibraryController(QtCore.QObject):

    def __init__(self, controller, ui):

        super().__init__()

        self.controller = controller
        self.ui = ui

        self.libraries = {}

        self.storage = GoogleStorage()

        folders = os.getenv('RD_LIBRARY')
        if not folders:
            return
        for folder in folders.split(':'):

            new_library = Library(folder)

            self.libraries[new_library.name] = new_library

            self.load_track_list(new_library)

            if self.storage.initialized:
                # host mode

                # assume that the local folder and the remote folder are in sync
            
                bucket = os.getenv('RD_STORAGE_GOOGLE_BUCKET')
                name = new_library.name 
                token = self.storage.token
                self.controller.social_controller.greetings.add(f'LIBRARY {bucket} {name} {token}')

    def receive(self, timetamp, sender, value):
        bucket, name, token = value.split(' ')

        for library in self.libraries:
            if (isinstance(library, RemoteLibrary) 
                    and library.bucket == bucket
                    and library.name == name):
                # library.token = token
                return
        else:
            new_library = RemoteLibrary(bucket, name, token)
            self.libraries[new_library.name] = new_library
            self.load_track_list(new_library)


    def load_track_list(self, library):
        index, track_list = self.ui.add_track_list(library.name)
        callback = partial(self.load_track, library_name=library.name)
        track_list.track_selected.connect(callback)

        self.ui.set_track_list(index, library.get_list())

    @QtCore.pyqtSlot(int, str)
    def load_track(self, deck=-1, name=None, library_name=None, send=True):

        if not name:
            raise Exception

        if deck < 0:
            deck = 0

        self.ui.decks[deck].track_info.setText('loading...')
        self.ui.decks[deck].repaint()

        if not library_name:
            # search everywhere
            library_name = self.find_name_in_library(name)

        track = self.libraries[library_name].get(name)

        if send is True:
            self.controller.send_load(deck, name)  # TODO load earlier

        self.controller.engine.load_track(deck, track)
        self.ui.decks[deck].track_info.setText(name)


    def find_name_in_library(self, name):
        for library in self.libraries.values():
            if name in library.tracks:
                return library.name
        else:
            raise Exception('File name not found in libraries')
