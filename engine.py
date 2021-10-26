import threading
import time


class Engine(threading.Thread):

    def __init__(self):
        super().__init__()

        self.running = False
        self.tempo_range = (33+8)/33 - 1

        self.start()

        while not self.running:
            time.sleep(.2)


    def run(self):

        self.players = {}

        self.running = True

        while True:
            time.sleep(1)

    def load_track(self, deck, filename):

        from player import Player

        if deck not in self.players:
            self.players[deck] = Player()

        self.players[deck].load_audio_file(filename)


    def play(self, deck, offset=None, timestamp=None):

        if offset is not None and timestamp:
            offset += time.time() - timestamp
            print(offset)

        self.players[deck].play(offset)


    def pause(self, deck):

        self.players[deck].pause()

    def change_tempo(self, deck, value):
        print(value)
        self.players[deck].tempo = 1 - self.tempo_range*value
