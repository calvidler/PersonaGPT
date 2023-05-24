from fastapi import APIRouter, Body, Response
from gtts import gTTS
import aiofiles
import os

# from bark import SAMPLE_RATE, generate_audio, preload_models
# from scipy.io.wavfile import write as write_wav
# from IPython.display import Audio

audio_router = APIRouter()


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
