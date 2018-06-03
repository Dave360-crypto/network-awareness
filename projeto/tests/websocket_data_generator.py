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
            max_int = 100
            min_int = 0

            if count < 10:
                max_int = 40
                min_int = 0
            elif 10 <= count < 20:
                max_int = 100
                min_int = 60
            else:
                count = 0

            others = random.randint(min_int, max_int)
            mining = 100 - others

            await websocket.send(json.dumps([mining, others]))

            time.sleep(1)
            count += 1

    start_server = websockets.serve(data, '127.0.0.1', 1234)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

