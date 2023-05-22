from fastapi import FastAPI
from fastapi.responses import RedirectResponse


from routes.text import text_router
from routes.audio import audio_router

app = FastAPI()


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


app.include_router(text_router, prefix="/text", tags=["text"])
app.include_router(audio_router, prefix="/audio", tags=["audio"])
