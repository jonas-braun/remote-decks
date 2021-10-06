#!/usr/bin/env python3

import os
import sys
import json
import asyncio
import datetime

import aio_pika


AMQP_HOST = os.getenv('AMQP_HOST')

class EventBus:

    def __init__(self, loop, controller):

        self.controller = controller

        self.exchange = None
        self.user_id = None
        
        task = asyncio.create_task(self.listen(loop))
        print('started listening')

    async def listen(self, loop):

        connection = await aio_pika.connect_robust(
                f'amqp://guest:guest@{AMQP_HOST}/', loop=loop
                )

        async with connection:

            channel = await connection.channel()
            self.exchange = await channel.declare_exchange('events', aio_pika.ExchangeType.FANOUT)


            queue = await channel.declare_queue(exclusive=True)
            print('QUEUE', queue)
            self.user_id = str(queue)

            await queue.bind(self.exchange)

            async with queue.iterator() as queue_iter:

                async for message in queue_iter:
                    
                    async with message.process():

                        print(str(datetime.datetime.now()))
                        print(message.correlation_id)
                        print(message.body.decode())

                        if not message.correlation_id == self.user_id:

                            body = message.body.decode()
                            timestamp = body[:17]
                            msg = body[18:]

                            self.controller.receive(timestamp, msg)


    def send_data(self, timestamp, msg):
        print('client send', msg)

        timestamped_message = f'{timestamp.timestamp():9.6f} {msg}' 

        if self.exchange:

            asyncio.create_task(self.client_send_data(timestamped_message))


    async def client_send_data(self, msg):
        await self.exchange.publish(
                aio_pika.Message(
                    body=msg.encode(),
                    correlation_id=self.user_id
                ),
                routing_key='',
        )
        print('ok')

