#!/usr/bin/env python3

import asyncio
import websockets
import argparse
import time
import datetime
import sys
import numpy as np
from scipy.io.wavfile import write
from pickle import dumps, loads

def parse_args(parser):
    parser.add_argument('-k', '--key', type=str,
                        help='API Key (ex: cfe79645h2ce1ce4d15jb21875078574)', required=True)
    parser.add_argument('-t', '--text', type=str, default='Salut, ce mai faci',
                        help='Input text')
    parser.add_argument('-o', '--output_filename', type=str, default="output_synth.wav",
                        help='Name of the output audio file (.wav)')
    parser.add_argument('-v', '--voice', type=str, default='gia',
                        help='Voice to use (FEMALE: ema, gia, maria; MALE: alex, radu)')
    parser.add_argument('-f', '--audio_format', type=str, default="WAV_PCM",
                        help='(optional) Audio format of the output audio (WAV_PCM, WAV_ULAW, WAV_ALAW, MP3)')
    parser.add_argument('-r', '--sample_rate', type=int, default=22050,
                        help='(optional) Sample rate of the output audio [Hz] (8000, 16000, 22050)')
    parser.add_argument('-p', '--pace', type=float, default=1.0,
                        help='(optional) Pace of the output audio [0.8->2.0]')
    parser.add_argument('-b', '--bits_per_sample', type=int, default=16,
                        help="Bits per sample of the output audio: 8, 16, 32")
    # parser.add_argument('--pitch-shift', type=float, default=0.0,
    #                        help='Raise/lower the pitch by <hz>')
    return parser

parser = argparse.ArgumentParser(description='TTS API Client', allow_abbrev=False)
parser = parse_args(parser)
args, _ = parser.parse_known_args()

sampling_rate = 22050

async def text2speech(uri):
    async with websockets.connect(uri, max_size= 10000000) as websocket:

        message = '{"task": [{"text": "' + args.text + '"}, {"voice": "'+ args.voice + '"}, {"key": "' + args.key + '"}, {"pace": "'+ str(args.pace) +'"}, {"audio_format": "'+ str(args.audio_format) +'"}, {"bits_per_sample": "' + str(args.bits_per_sample) + '"}, {"sample_rate": "'+ str(args.sample_rate) +'"}]}'
        await websocket.send(message)
        result = await websocket.recv()
        if isinstance(result, str):
            print(result)
        else:
            binary_file = open(args.output_filename, "wb")
            binary_file.write(result)
            binary_file.close()
            print ("DONE!")

asyncio.get_event_loop().run_until_complete(
        text2speech('wss://api-tts.zevo-tech.com:2053'))
