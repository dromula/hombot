import websockets
import asyncio
import json
from robot import Robot, Direction
import logging

class RobotClient():

    def __init__(self):
        self.robot = Robot()

    async def connect(self):
        '''
            Connecting to webSocket server

            websockets.client.connect returns a WebSocketClientProtocol, which is used to send and receive messages
        '''
        self.connection = await websockets.client.connect('ws://127.0.0.1:6789')
        if self.connection.open:
            print('Connection stablished. Client correcly connected')
            # Send greeting
            await self.sendMessage('Hey server, this is webSocket client')
            return self.connection


    async def sendMessage(self, message):
        '''
            Sending message to webSocket server
        '''
        await self.connection.send(message)

    async def send_error(self, message: str):
        logging.error(f"unsupported event: {message}")
        await self.sendMessage(json.dumps({"type": "error", "msg": message}))

    async def recv_set_robot(self, data: any):
        if data["motor"] == "left":
            self.robot.set_left(int(data["power"]))
        elif data["motor"] == "right":
            self.robot.set_right(int(data["power"]))

    async def receiveMessage(self, connection):
        '''
            Receiving all server messages and handling them
        '''
        while True:
            try:
                message = await connection.recv()
                print("Received: " + str(message))

                data = json.loads(message)
                if data["type"] == "req_role":
                    await self.sendMessage(json.dumps({ "type": "resp_role", "role": "robot"}))
                elif data["type"] == "set_robot":
                    await self.recv_set_robot(data)
                elif data["type"] == "error":
                    logging.error(data["msg"])
                else:
                    await self.send_error(data)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break

    async def heartbeat(self, connection):
        '''
        Sending heartbeat to server every 5 seconds
        Ping - pong messages to verify connection is alive
        '''
        while True:
            try:
                await connection.send(json.dumps({"type": "ping_motor"}))
                await asyncio.sleep(10)
            except websockets.exceptions.ConnectionClosed:
                print('Connection with server closed')
                break
