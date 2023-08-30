from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import speech_recognition as sr
from flask import Flask, jsonify
from flask_restful import Api, Resource
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import speech_recognition as sr
from flask_restful import Api, Resource
import asyncio
import websockets
import warnings
from urllib3.exceptions import InsecureRequestWarning
import os

#chatbot imports
import asyncio
import websockets
import speech_recognition as sr
#import requests
import warnings
import json
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)
import urllib3
import urllib
import os
import sys
from timeit import default_timer as timer
from scipy.io.wavfile import write
from pickle import dumps, loads

from concurrent.futures import ThreadPoolExecutor
import pygame

executor = ThreadPoolExecutor()


app = Flask(__name__)
api = Api(app)
CORS(app) 

# Route for the root
@app.route('/')
def index():
    return render_template('index.html')

# Route for the favicon.ico (if you have one in the static folder)
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


class AnswerQuestion(Resource):
    def get(self):
        encyclopedia = {
            "aş dori să fac o programare": "Bună ziua! În cele ce urmează, vom crea o nouă programare! Va rog specificați orașul în care va aflați",
            "bucureşti": "Vă rog specificați una dintre următoarele specializări: cardiologie, oftalmologie, pediatrie",
            "argovişte": "Ne pare rău, această clinică nu există în Târgoviște.",
            "cardiologie": "Pentru cardiologie, avem disponibile următoarele intervale: marti 10:00 - 11:00, joi 14:00 - 15:00. Va rog alegeți unul dintre intervale.",
            "oftalmologie": "Pentru oftalmologie, avem disponibile următoarele intervale: marti 11:00 - 12:00, joi 13:00 - 14:00. Va rog alegeți unul dintre intervale.",
            "marţi zece unsprezece": "Aveți o programare la cardiologie, marți 10:00 - 11:00, domnul doctor Y, la sediul din Calea Griviței, numărul 23, București.Confirmaţi această programare?",
            "marţi unsprezece doisprezece": "Aveti o programare la oftalmologie, marti 10:00 - 11:00, domnul doctor X, la sediul din Calea Grivitei, numarul 23, București.Confirmaţi această programare?",
            "joi paisprezece cincispreze": "Aveti o programare la cardiologie, marti 10:00 - 11:00, domnul doctor Y, la sediul din Calea Grivitei, numarul 23, București.Confirmaţi această programare?",
            "joi treisprezece paisprezece": "Aveti o programare la oftalmologie, marti 10:00 - 11:00, domnul doctor X, la sediul din Calea Grivitei, numarul 23, București.Confirmaţi această programare?",
            "da": "Va rog să rostiți numele dumneavoastră.",
            "popescu ion":"Va rog să rostiți numărul dumneavoastră de telefon.",
            "zero şapte doi":"Dacă datele sunt corecte, va rugăm rostiți cuvântul corect. Altfel rostiți cuvântul incorect.",
            "corect":"Programarea dumneavoastră a fost confirmată pe numele Popescu Ion. Va dorim o zi bună!",
            "care este teorema lui pitagora": "În orice triunghi dreptunghic, suma pătratelor catetelor este egală cu pătratul ipotenuzei.",
            "deschide geamul din dreapta faţă": "Am deschis geamul din dreapta față.",
            "închide geamul din dreapta faţă": "Am închis geamul din dreapta față.",
            "deschide geamul din stânga spate": "Am deschis geamul din stânga spate.",
            "închide geamul din stânga spate": "Am închis geamul din stânga spate.",
            "porneşti aerul condiţionat": "Am pornit aerul condiționat.",
            "opreşte aerul condiţionat": "Am oprit aerul condiționat.",
            "setează aerul condiţionat pe douăzeci şi unu de grade": "Am setat aerul condiționat pe douăzeci și unu de grade.",
            "vreau să ascult radio zu": "Am pornit radio zu.",
            "vreau să ascult radio zu"
            "bucureşti condiţionat"
            "vreau să ascult radio europa fm": "Am pornit radio europa efem.",
            "vreau să ascult radio europa efem": "Am pornit radio europa efem."


        }


        # Mute ALSA output from the driver
        import ctypes

        ERROR_HANDLER_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p, ctypes.c_int,
                                            ctypes.c_char_p, ctypes.c_int,
                                            ctypes.c_char_p)


        # if len(sys.argv) != 2:
        #     print("Usage: chatbot.py <api_key>")
        #     exit(0)

        key = 'acdragan@2023' #sys.argv[1]



        def py_error_handler(filename, line, function, err, fmt):
            pass


        c_error_handler = ERROR_HANDLER_FUNC(py_error_handler)

        try:
            asound = ctypes.cdll.LoadLibrary('libasound.so.2')
            asound.snd_lib_error_set_handler(c_error_handler)
        except OSError:
            pass


        async def speech_to_text_ws(audio):
            uri = 'wss://live-transcriber.zevo-tech.com:2053'
            sample_rate = 16000

            async with websockets.connect(uri) as websocket:
                await websocket.send('{"config": {"key": "' + key + '"}}')
                print(await websocket.recv())
                await websocket.send('{"config": {"sample_rate": "' + str(sample_rate) + '"}}')
                print(await websocket.recv())
                while (len(audio) > 0):
                    data = audio[:16000]
                    await websocket.send(data)
                    await websocket.recv()
                    audio = audio[16000:]

                await websocket.send('{"eof" : 1}')
                result_json = json.loads(await websocket.recv())
                return result_json["text"]



        async def text2speech(text):
            uri = 'wss://api-tts.zevo-tech.com:2083'
            voice = 'ema'
            sampling_rate = 22050
            filename = 'temp.wav'

            async with websockets.connect(uri) as websocket:

                message = '{"task": [{"text": "' + text + '"}, {"voice": "'+ voice + '"}, {"key": "' + key + '"}]}'
                await websocket.send(message)
                result = await websocket.recv()
                if isinstance(result, str):
                    print(result)
                else:
                    binary_file = open(filename, "wb")
                    binary_file.write(result)
                    binary_file.close()
                    print ("DONE!")
                return filename


        def answerQuestion():
            r = sr.Recognizer()

            with sr.Microphone(sample_rate=16000) as source:
                print('Ask a question...')
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source)
                start_time = timer()

            try:
                future = executor.submit(asyncio.run, speech_to_text_ws(audio.get_wav_data()))
                question = future.result()
                question.strip()
                print('Question: ' + question)
                print("DEBUG: elapsed time " +
                    "{:.2f}".format(timer() - start_time) + "s")

                try:
                    answer = encyclopedia[question]
                except KeyError:
                    answer = "Nu știu să răspund la această întrebare"
                print('Answer: ')

                future = executor.submit(asyncio.run, text2speech(answer))
                spoken_answer_url = future.result()

                print("DEBUG: elapsed time " +
                    "{:.2f}".format(timer() - start_time) + "s")
                
                print("Playing audio answer...")
                pygame.mixer.init()  # Initialize the mixer
                pygame.init()
                # Load the WAV file
                sound = pygame.mixer.Sound(r"temp.wav")
                # Play the sound
                sound.play()
                # Wait for the sound to finish playing
                pygame.time.wait(int(sound.get_length() * 1000))  # Convert to milliseconds
                pygame.mixer.quit()  # Quit the mixer
                pygame.quit()
                print("mplayer " + spoken_answer_url + " > /dev/null 2>&1")
                
                # os.system("mplayer " + spoken_answer_url + " > /dev/null 2>&1")
                print("DEBUG: elapsed time " +
                    "{:.2f}".format(timer() - start_time) + "s")

                print("\n\n\n---------------------------")
            except sr.UnknownValueError:
                print('.... can`t understand')

            return answer, question

        try:
            # Run your function
            answer, question = answerQuestion()
            return jsonify({
                "status": "success",
                "question": question,  # Modify this as per your logic if required
                "answer": answer
            })
        except Exception as e:
            return jsonify({
                "status": "error",
                "message": str(e)
            })
            
            
api.add_resource(AnswerQuestion, '/answer')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
