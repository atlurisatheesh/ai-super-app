# from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
# from fastapi.middleware.cors import CORSMiddleware
# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from slowapi.errors import RateLimitExceeded
# from slowapi.middleware import SlowAPIMiddleware
# from fastapi.responses import JSONResponse
# from openai import OpenAI
# import numpy as np
# import soundfile as sf
# import io
# import asyncio
# import openai
# import os
# import whisper
# import tempfile

# openai.api_key = os.getenv("OPENAI_API_KEY")
# from api import chat, live, dev, creative, image  # ✅ image added
# client = OpenAI()
# app = FastAPI(title="AI Super App")

# # ✅ CORS (THIS FIXES OPTIONS 405)
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],  # frontend
#     # allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# limiter = Limiter(key_func=get_remote_address)
# app.state.limiter = limiter
# app.add_middleware(SlowAPIMiddleware)

# @app.exception_handler(RateLimitExceeded)
# def rate_limit_handler(request, exc):
#     return JSONResponse(
#         status_code=429,
#         content={"error": "Too many requests. Please slow down."}
#     )

# # ✅ API ROUTERS
# app.include_router(chat.router)
# app.include_router(live.router)
# app.include_router(dev.router)
# app.include_router(creative.router)
# app.include_router(image.router)   # ✅ image router added

# @app.get("/")
# def health():
#     return {"status": "ok"}
# # @app.post("/image")
# # def generate_image(prompt: str):
# #     result = client.images.generate(
# #         model="gpt-image-1",
# #         prompt=prompt,
# #         size="1024x1024"
# #     )
# #     return {"url": result.data[0].url}

# # app = FastAPI()

# @app.websocket("/ws/stt")
# async def ws_stt(ws: WebSocket):
#     await ws.accept()
#     buffer = bytearray()

#     while True:
#         chunk = await ws.receive_bytes()
#         buffer.extend(chunk)

#         if len(buffer) > 16000 * 2 * 3:  # 3 seconds
#             audio = np.frombuffer(buffer, dtype=np.int16).astype(np.float32) / 32768.0
#             buffer.clear()

#             wav = io.BytesIO()
#             sf.write(wav, audio, 16000, format="WAV")
#             wav.seek(0)

#             try:
#                 resp = openai.audio.transcriptions.create(
#                     file=wav,
#                     model="whisper-1"
#                 )
#                 await ws.send_text(resp.text)
#             except Exception as e:
#                 print("❌ Whisper:", e)

#     @app.post("/api/stt")
#     async def speech_to_text(file: UploadFile = File(...)):
#     # Save audio temporarily
#         with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp:
#             tmp.write(await file.read())
#             tmp_path = tmp.name

#     # # Whisper transcription
#     # with open(tmp_path, "rb") as audio_file:
#     #     transcript = openai.audio.transcriptions.create(
#     #         file=audio_file,
#     #         model="whisper-1"
#     #     )
#     result = whisper_model.transcribe(tmp_path)

#     return {"text": result["text"]}



from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

import numpy as np
import soundfile as sf
import io
import os
import tempfile
import whisper
import openai

from api import chat, live, dev, creative, image

# =====================
# APP SETUP (ONLY ONCE)
# =====================
app = FastAPI(title="AI Super App")

# =====================
# CORS
# =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================
# RATE LIMITING
# =====================
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests. Please slow down."}
    )

# =====================
# LOAD WHISPER ONCE
# =====================
whisper_model = whisper.load_model("base")

# =====================
# ROUTERS (UNCHANGED)
# =====================
app.include_router(chat.router)
app.include_router(live.router)
app.include_router(dev.router)
app.include_router(creative.router)
app.include_router(image.router)

# =====================
# HEALTH
# =====================
@app.get("/")
def health():
    return {"status": "ok"}

# =====================
# WEBSOCKET STT (LIVE)
# =====================
@app.websocket("/ws/stt")
async def ws_stt(ws: WebSocket):
    await ws.accept()
    buffer = bytearray()

    try:
        while True:
            chunk = await ws.receive_bytes()
            buffer.extend(chunk)

            if len(buffer) > 16000 * 2 * 3:  # ~3 seconds
                audio = np.frombuffer(buffer, dtype=np.int16).astype(np.float32) / 32768.0
                buffer.clear()

                wav = io.BytesIO()
                sf.write(wav, audio, 16000, format="WAV")
                wav.seek(0)

                try:
                    result = whisper_model.transcribe(wav)
                    await ws.send_text(result["text"])
                except Exception as e:
                    await ws.send_text(f"❌ Whisper error: {e}")

    except WebSocketDisconnect:
        print("🔌 WS disconnected")

# =====================
# HTTP WHISPER STT (STEP 3B)
# =====================
@app.post("/api/stt")
async def speech_to_text(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1] or ".wav"
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    result = whisper_model.transcribe(tmp_path)
    os.unlink(tmp_path)

    return {"text": result["text"]}
