import requests
import json

with open('output.mp3', 'rb') as file:
    audio_data = file.read()

url = "http://0.0.0.0:8000/audio/speech-to-text/"
files = {'in_file': ('output.mp3', audio_data)}

response = requests.post(url, files=files)

print(response.json())