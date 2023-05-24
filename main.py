from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

from routes.text import text_router
from routes.audio import audio_router
from routes.websocket import websocket_router

app = FastAPI()


@app.get("/")
async def docs_redirect():
    return RedirectResponse(url="/docs")


app.include_router(text_router, prefix="/text", tags=["text"])
# app.include_router(audio_router, prefix="/audio", tags=["audio"])
app.include_router(websocket_router, prefix="", tags=["ws"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
