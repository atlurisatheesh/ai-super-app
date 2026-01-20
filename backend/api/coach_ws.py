# from fastapi import WebSocket
# import numpy as np

# @app.websocket("/ws/coach")
# async def coach_ws(ws: WebSocket):
#     await ws.accept()

#     audio_buffer = []

#     try:
#         while True:
#             chunk = await ws.receive_bytes()
#             audio = np.frombuffer(chunk, dtype=np.float32)
#             audio_buffer.append(audio)

#             # simple silence detection
#             if len(audio_buffer) > 20:
#                 text = transcribe(audio_buffer)
#                 await ws.send_json({"type": "transcript", "text": text})
#                 audio_buffer.clear()

#     except Exception:
#         pass

from fastapi import APIRouter, WebSocket
import numpy as np
import whisper

router = APIRouter()
model = whisper.load_model("tiny")

@router.websocket("/api/stt")
async def stt_ws(ws: WebSocket):
    await ws.accept()
    print("🎧 STT WS CONNECTED")

    audio_buffer = []

    try:
        while True:
            data = await ws.receive_bytes()
            print("RECEIVED BYTES:", len(data))

            audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
            audio_buffer.append(audio)

            # ✅ IMPORTANT: enough audio
            if sum(len(a) for a in audio_buffer) > 32000:
                samples = np.concatenate(audio_buffer)
                audio_buffer.clear()

                result = model.transcribe(samples, fp16=False)
                text = result.get("text", "").strip()

                if text:
                    print("TRANSCRIPT:", text)
                    await ws.send_json({ "text": text })

    except Exception as e:
        print("STT WS ERROR:", e)
        await ws.close()

