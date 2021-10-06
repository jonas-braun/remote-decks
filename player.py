import math

import numpy as np

import soundfile as sf
import sounddevice as sd

import samplerate as sr


class Player:

    blocksize = 1024

    def __init__(self):

        self.sample_rate = 44100

        self.position = -1
        self.volume = 1
        self.tempo = 1

        self.buffer = np.zeros((self.blocksize, 2), dtype='float32')

        self.audio_file = None
        self.stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=2,
                blocksize=self.blocksize,
                callback=self.callback_closure()
                )


    def callback_closure(self):
        position = -1

        def callback(outdata, frames, time, status):
            nonlocal position

            frames_to_read = math.ceil(frames/self.tempo)

            data = self.audio_file.read(frames_to_read, fill_value=0) * self.volume

            data = sr.resample(data, self.tempo, 'sinc_best')[:self.blocksize]

            self.buffer[:data.shape[0], :] = data

            outdata[:] = self.buffer

        return callback


    def load_audio_file(self, filename):

        self.audio_file = sf.SoundFile(filename)


    def play(self):
        # TODO seek
        self.stream.start()

    def pause(self):
        self.stream.stop()  # TODO resync
