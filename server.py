import asyncio
import websockets
import requests
import json
import time

API_KEY = " "  
TARGET = "KZT"                      
cache = {}
last_time = 0

def get_rate(base: str):
    global cache, last_time

    if (base not in cache) or (time.time() - last_time > 60):
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base}"
        try:
            response = requests.get(url, timeout=5)
            data = response.json()

            if data["result"] == "success":
                rate = data["conversion_rates"][TARGET]
                cache[base] = rate
                last_time = time.time()
            else:
                return {"error": f"API error: {data}"}
        except Exception as e:
            return {"error": str(e)}

    return {f"{base}->{TARGET}": cache[base]}

async def handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            module = data.get("module")

            if module == "ping":
                await websocket.send(json.dumps({"status": "pong"}))

            elif module == "info":
                base = data.get("base", "USD")  
                rate_info = get_rate(base)
                await websocket.send(json.dumps(rate_info))

            else:
                await websocket.send(json.dumps({"error": "unknown module"}))

        except Exception as e:
            await websocket.send(json.dumps({"error": f"bad request: {str(e)}"}))

async def main():
    async with websockets.serve(handler, "localhost", 5001):
        await asyncio.Future()

asyncio.run(main())

