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

        from player import Player

        self.player_1 = Player()
        self.player_1.load_audio_file('data/test.wav')

        self.running = True

        while True:
            time.sleep(1)


    def play(self, offset=.0):

        self.player_1.play()


    def pause(self):

        self.player_1.pause()

    def change_tempo(self, value):
        print(value)
        self.player_1.tempo = 1 - self.tempo_range*value
