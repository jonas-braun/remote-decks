#!/usr/bin/env python3

import time

from player import Player



player_1 = Player()

player_1.load_audio_file('data/test.wav')

player_2 = Player()

player_2.load_audio_file('data/test.wav')

start_time = time.time()

player_1.play()


time.sleep(5)


player_2.play(5.)
#player_1.pause()

time.sleep(5)

end_time = time.time()

print(end_time - start_time)
