import requests
import json

response = requests.post(
    "http://127.0.0.1:8000/audio/text-to-speech/",
    data=json.dumps({"text": "Hello world"}),
)
print(response)

# Ensure the request was successful
response.raise_for_status()

# Open the file in write-bytes mode
with open("output.mp3", "wb") as output_file:
    # Write the response content to the file
    output_file.write(response.content)
