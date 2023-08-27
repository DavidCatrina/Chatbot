#!/usr/bin/env python3

import asyncio
import websockets
import sys

if len(sys.argv) != 5:
    print("Usage: STT.py <filename> <language> <api-key> <sample-rate>")
    print("<filename> path audio file")
    print("<language> romanian and english are available")
    print("<sample_rate> could be 16000 or 8000")
    exit(0)


filename = sys.argv[1]
language = sys.argv[2]
key = sys.argv[3]
sample_rate = sys.argv[4]

if language == "romanian":
    server_address = "wss://live-transcriber.zevo-tech.com:2053"
elif language == "english":
    server_address = "wss://en-live-transcriber.zevo-tech.com:2083"

async def speechtotext(uri):
    async with websockets.connect(uri) as websocket:

    ## Send the API key
        await websocket.send('{"config": {"key": "' + key + '"}}')
        result_text = await websocket.recv()
        print(result_text)
        if "error" in result_text:
            exit()
            
    ## Set the sample rate
        await websocket.send('{"config": {"sample_rate": "' + str(sample_rate) + '"}}')
        result_text = await websocket.recv()
        print(result_text)
        if "error" in result_text:
            exit()

    ## Send audio data
        wf = open(filename, "rb")
        while True:
            data = wf.read(16000)

            if len(data) == 0:
                break

            await websocket.send(data)
            result_text = await websocket.recv()
            print(result_text)
            if "error" in result_text:
                exit()

    ## Send end of stream signal
        await websocket.send('{"eof" : 1}')
        print (await websocket.recv())

asyncio.get_event_loop().run_until_complete(
    speechtotext(server_address))
