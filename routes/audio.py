from fastapi import APIRouter, Body, Response
from gtts import gTTS
import aiofiles
import os

audio_router = APIRouter()


@audio_router.post("/text-to-speech/")
async def text_to_speech(body: dict = Body(...)):
    # TODO add
    text = body["text"]
    agent_id = body.get("agent_id")
    tts = gTTS(text=text, lang="en")
    filename = "speech.mp3"
    tts.save(filename)

    async with aiofiles.open(filename, mode="rb") as f:
        content = await f.read()
    os.remove(filename)

    return Response(content, media_type="audio/mpeg")
