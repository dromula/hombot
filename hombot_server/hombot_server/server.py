import asyncio
import json
import logging
import websockets
from websockets import WebSocketServerProtocol

logging.basicConfig(level=logging.INFO)

controller = WebSocketServerProtocol
robot = WebSocketServerProtocol

async def register(socket):
    await socket.send(json.dumps({"type": "req_role"}))


async def unregister(websocket):
    pass

async def set_role(socket: WebSocketServerProtocol, role: str ):
    global controller
    global robot
    if role == "controller":
        controller = socket
        logging.info("Controller connected!")
    elif role == "robot":
        robot = socket
        print("Motor connected!")
    else:
        await send_error(socket, "Unsupported role!")

async def send_error(socket: WebSocketServerProtocol, message: str):
    logging.error(f"unsupported event: {message}")
    await socket.send(json.dumps({"type": "error", "msg": message}))

async def recv_by_robot():
    pass

async def recv_by_controller(message: str):
    data = json.loads(message)
    if data["type"] == "set_robot":
        await robot.send(message)


async def counter(websocket, path):
    # register(websocket) sends user_event() to websocket
    await register(websocket)
    try:
        async for message in websocket:
            print("Received: " + str(message))
            try:
                data = json.loads(message)
                if websocket == controller:
                    await recv_by_controller(message)
                elif data["type"] == "resp_role":
                    await set_role(websocket, data["role"])
                elif data["type"] == "error":
                    logging.error(data["msg"])
                else:
                    await send_error(websocket, data)
            except:
                pass
    finally:
        await unregister(websocket)
        
start_server = websockets.serve(counter, "localhost", 6789)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()