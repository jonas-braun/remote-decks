#!/usr/bin/env python3

import time

from engine import Engine


e = Engine()

e.load_track(0, 'data/test.wav')
e.load_track(1, 'data/test.wav')

start_time = time.time()
e.play(0, 0., start_time)

time.sleep(5)

#e.play(1, 5.)
end_time = time.time()

#e.play(1, end_time - start_time)
e.play(1, 0., start_time)
#e.play(0, 0., time.time()-5)
