import asyncio
import websockets
import json

async def main():
    async with websockets.connect("ws://localhost:5001") as ws:
        await ws.send(json.dumps({"id": 1, "module": "ping"}))
        print(await ws.recv())

        await ws.send(json.dumps({"id": 2, "module": "info", "base": "USD"}))
        print(await ws.recv())

asyncio.run(main())
