#!/usr/bin/env python3

import sys
import json
import time
import asyncio
import datetime
import threading

from PyQt5 import QtWidgets
from qasync import QEventLoop

from controller import Controller
from engine import Engine




def main():
    app = QtWidgets.QApplication(sys.argv)
    loop = QEventLoop(app)

    asyncio.set_event_loop(loop)

    engine = Engine()

    controller = Controller(app, loop, engine)
    
    with loop:

        loop.run_forever()
        



if __name__ == '__main__':
    main()
