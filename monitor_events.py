#!/usr/bin/env python3

import time
import asyncio

from events import EventBus


class TestController():

    def receive(self, timestamp, sender, msg):
        runtime = time.time() - timestamp
        print(timestamp, sender, msg)
        print('Runtime', runtime)

async def main():
    loop = asyncio.get_event_loop()

    controller = TestController()

    event_bus = EventBus(loop, controller)

    await asyncio.sleep(100000)


if __name__ == '__main__':

    loop = asyncio.get_event_loop()

    asyncio.run(main())

    loop.run_forever()
