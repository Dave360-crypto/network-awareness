import time
import asyncio
import websockets
import json
import random


count = 0


if __name__ == '__main__':

    async def data(websocket, path):
        global count

        while True:
            data = {
                "443": "Not enough data (118)",
                "49180": "Not enough data (1)",
                "50641": "Not enough data (1)",
                "50646": {
                    "Mining": 80.0,
                    "Other": 20.0
                },
                "57377": "Not enough data (1)",
                "61578": "Not enough data (1)",
                "80": {
                    "Mining": 50.0,
                    "Other": 50.0
                },
                "993": "Not enough data (1)"
            }

            await websocket.send(json.dumps(data))

            time.sleep(1)
            count += 1

    start_server = websockets.serve(data, '127.0.0.1', 1234)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

