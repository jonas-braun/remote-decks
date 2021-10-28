#!/usr/bin/env python3

import time
import asyncio

from events import EventBus


class TestController():

    def receive(timestamp, msg):
        print(timestamp, msg)

async def main():
    loop = asyncio.get_event_loop()

    controller = TestController()

    event_bus = EventBus(loop, controller)

    await asyncio.sleep(5)

    timestamp = time.time()
    event_bus.send_data(timestamp, 'PLAY 0 10.0')


if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    asyncio.run(main())

    loop.run_forever()
