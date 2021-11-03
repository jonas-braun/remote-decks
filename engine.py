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
            self.players[deck] = Player(deck)

        self.players[deck].load_audio_file(filename)


    def play(self, deck, offset=None, timestamp=None):
        """
        Offset is the position in the track where the playback is supposed to start.
        timestamp is the time when that playback was supposed to start, so it can be used to
        adjust the offset so that it accounts for any time lag in the communication.
        """

        if offset is not None and timestamp:
            offset += time.time() - timestamp
            print(offset)

        self.players[deck].play(offset)


    def pause(self, deck):

        self.players[deck].pause()

    def change_tempo(self, deck, value, timestamp=None):
        print(value)
        tempo = 1 - self.tempo_range*value
        if timestamp:
            offset = time.time() - timestamp
            self.players[deck].set_tempo(tempo, offset)
        else:
            self.players[deck].tempo = tempo
