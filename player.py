import math

import numpy as np

import soundfile as sf
import sounddevice as sd

import samplerate as sr


class OutputFile:
    def __init__(self, samplerate, channels, blocksize, callback):
        self.output_file = sf.SoundFile('output.wav',
                mode='w',
                samplerate=samplerate,
                channels=channels,
                format='WAVEX')


class Player:

    """
    The Player represents one input audio file and one audio output.
    It should run in a separate thread so it can resample audio data without causing a buffer
    underrun. The output interface is configurable especially for testing purposes.
    """

    blocksize = 1024

    def __init__(self, deck=None):

        self.deck = deck

        self.sample_rate = 44100

        self.position = -1
        self.volume = 1
        self.tempo = 1

        self.is_playing = False

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

    def get_position(self):
        return self.audio_file.tell() / self.sample_rate

    def set_tempo(self, tempo, offset):
        position = self.audio_file.tell() / self.sample_rate
        corrected_position = position + (offset * (tempo - self.tempo))
        self.audio_file.seek(int(corrected_position * self.sample_rate))
        self.tempo = tempo

    def play(self, offset=None):
        self.is_playing = True
        if offset:
            pos = int(offset * self.sample_rate)
            self.audio_file.seek(pos)
        self.stream.start()

    def pause(self):
        self.is_playing = False
        self.stream.stop()  # TODO resync
