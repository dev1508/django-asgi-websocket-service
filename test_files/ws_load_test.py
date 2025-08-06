import asyncio
import websockets

URI = "ws://localhost:8080/ws/chat/"

async def connect(client_id):
    try:
        async with websockets.connect(URI) as websocket:
            await asyncio.sleep(10)  # Keep connection open
    except Exception as e:
        print(f"Client {client_id} failed: {e}")

async def main():
    total_clients = 5000
    print(f"Spawning {total_clients} concurrent WebSocket connections...")
    await asyncio.gather(*(connect(i) for i in range(total_clients)))

if __name__ == "__main__":
    asyncio.run(main())
