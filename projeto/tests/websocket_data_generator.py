import time
import asyncio
import websockets
import json
import random


if __name__ == '__main__':

    async def data(websocket, path):
        while True:
            others = random.randint(0, 100)
            mining = 100 - others

            await websocket.send(json.dumps([mining, others]))

            time.sleep(0.5)

    start_server = websockets.serve(data, '127.0.0.1', 1234)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

