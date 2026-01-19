from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI

from api import chat, live, dev, creative, image  # ✅ image added
client = OpenAI()
app = FastAPI(title="AI Super App")

# ✅ CORS (THIS FIXES OPTIONS 405)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests. Please slow down."}
    )

# ✅ API ROUTERS
app.include_router(chat.router)
app.include_router(live.router)
app.include_router(dev.router)
app.include_router(creative.router)
app.include_router(image.router)   # ✅ image router added

@app.get("/")
def health():
    return {"status": "ok"}
# @app.post("/image")
# def generate_image(prompt: str):
#     result = client.images.generate(
#         model="gpt-image-1",
#         prompt=prompt,
#         size="1024x1024"
#     )
#     return {"url": result.data[0].url}