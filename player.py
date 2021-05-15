import math

import soundfile as sf
import sounddevice as sd

import samplerate as sr


class Player:

    def __init__(self):

        self.sample_rate = 44100

        self.position = -1
        self.volume = 1
        self.tempo = 1

        self.audio_file = None
        self.stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=2,
                blocksize=2048,
                callback=self.callback_closure()
                )


    def callback_closure(self):
        position = -1

        def callback(outdata, frames, time, status):
            nonlocal position

            frames_to_read = math.ceil(frames/self.tempo)

            data = self.audio_file.read(frames_to_read, fill_value=0) * self.volume

            data = sr.resample(data, self.tempo, 'sinc_best')

            outdata[:] = data

        return callback


    def load_audio_file(self, filename):

        self.audio_file = sf.SoundFile(filename)


    def play(self):
        self.stream.start()
