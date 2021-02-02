import RPi.GPIO as io
import time
from enum import Enum
import asyncio
from websocket_client import RobotClient
from robot import Robot
import logging

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    # Creating client object
    client = RobotClient()
    loop = asyncio.get_event_loop()
    # Start connection and get client connection protocol
    connection = loop.run_until_complete(client.connect())
    # Start listener and heartbeat 
    tasks = [
        #asyncio.ensure_future(client.heartbeat(connection)),
        asyncio.ensure_future(client.receiveMessage(connection)),
    ]

    loop.run_until_complete(asyncio.wait(tasks))
