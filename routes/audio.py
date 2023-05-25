from fastapi import APIRouter, Body, Response, File, UploadFile
from gtts import gTTS
import aiofiles
import os

import whisper
import uuid
import os.path

# from bark import SAMPLE_RATE, generate_audio, preload_models
# from scipy.io.wavfile import write as write_wav
# from IPython.display import Audio

audio_router = APIRouter()

# Load Model
whisper_model = whisper.load_model("base")

@audio_router.post("/text-to-speech/")
async def text_to_speech(body: dict = Body(...)):
    # TODO add
    text = body["text"]
    agent_id = body.get("agent_id")
    
    tts = gTTS(text=text, lang="en")
    filename = "speech.mp3"
    tts.save(filename)

    # download and load all models
    # preload_models()

    # # generate audio from text
    # audio_array = generate_audio(text)

    # # save audio to disk
    # write_wav(filename, SAMPLE_RATE, audio_array)
    
    # play text in notebook
    # Audio(audio_array, rate=SAMPLE_RATE)


    async with aiofiles.open(filename, mode="rb") as f:
        content = await f.read()
    os.remove(filename)

    return Response(content, media_type="audio/mpeg")

@audio_router.post("/speech-to-text/")
async def speech_to_text(in_file: UploadFile = File(...)):

    # Upload and save the file to disk
    try:
        contents = await in_file.read()
        extension = os.path.splitext(in_file.filename)[1]

        tmp_filename = str(uuid.uuid4()) + extension
        with open(tmp_filename, 'wb') as f:
            f.write(contents)
    except Exception as e:
        return {"message": f"There was an error uploading the file {in_file.filename}; {e}"}
    
    finally:
        in_file.file.close()

    # Transcribe the audio file
    try:
        result = whisper_model.transcribe(tmp_filename)
    except Exception as e:
        return {"message": f"There was an error transcribing the file {in_file.filename}; {e}"}
    finally:
        # Delete the temporary file
        os.remove(tmp_filename)

    return {'message': result["text"]}

