# import asyncio
# import websockets
# import json
#
# async def test_chat():
#     uri = "ws://localhost:8000/ws/chat/"
#     async with websockets.connect(uri) as websocket:
#         await websocket.send("hello")
#         print("<", await websocket.recv())
#
#         await websocket.send("hi again")
#         print("<", await websocket.recv())
#
#         await websocket.send("final msg")
#         print("<", await websocket.recv())
#
#         # 🔁 Send quit message to close gracefully
#         await websocket.send("quit")
#         print("<", await websocket.recv())
#
#         # Confirm connection closes after bye
#         try:
#             await websocket.recv()
#         except websockets.exceptions.ConnectionClosedOK:
#             print("Connection closed gracefully.")
#
# asyncio.run(test_chat())


import asyncio
import websockets

async def test_chat():
    uri = "ws://localhost:8000/ws/chat/"
    async with websockets.connect(uri) as websocket:
        while True:
            msg = await websocket.recv()
            print("<", msg)

asyncio.run(test_chat())