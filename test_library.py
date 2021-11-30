#!/usr/bin/env python3

import os

from library import Library



l = Library(os.getenv('RD_LIBRARY').split(':')[0])

print(l.tracks)
