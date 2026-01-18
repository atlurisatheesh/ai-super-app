from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.core.intent import intent
from app.core.router import run, run_stream
from app.models.schemas import ChatReq, ChatRes

router = APIRouter()


# -----------------------------
# Helper: build hidden file context
# -----------------------------
def build_file_context(files) -> str:
    if not files:
        return ""

    context = ""
    for f in files:
        # f is a Pydantic FileItem object
        name = f.name
        text = f.text

        context += (
            f"Document name: {name}\n"
            f"Content:\n{text}\n\n"
        )

    return context



# -----------------------------
# Normal (non-stream) chat
# -----------------------------
@router.post("/", response_model=ChatRes)
def chat(req: ChatReq):
    mode = req.mode if req.mode != "auto" else intent(req.message)

    # ✅ NEW: hidden file context (safe, additive)
    file_context = build_file_context(
        getattr(req, "files", None)
    )

    # ✅ If files exist, prepend as system context
    final_message = (
        f"You are an assistant with access to the following documents:\n\n"
        f"{file_context}\n"
        f"User message:\n{req.message}"
        if file_context
        else req.message
    )

    return ChatRes(
        reply=run(mode, final_message)
    )


# -----------------------------
# Streaming chat (typing effect)
# -----------------------------
@router.post("/stream")
def chat_stream(req: ChatReq):
    mode = req.mode if req.mode != "auto" else intent(req.message)

    # ✅ NEW: hidden file context (safe, additive)
    file_context = build_file_context(
        getattr(req, "files", None)
    )

    final_message = (
        f"You are an assistant with access to the following documents:\n\n"
        f"{file_context}\n"
        f"User message:\n{req.message}"
        if file_context
        else req.message
    )

    # 🔎 DEBUG (remove later if you want)
    if file_context:
        print("FILES RECEIVED IN /stream:", len(req.files))

    return StreamingResponse(
        run_stream(mode, final_message),
        media_type="text/plain"
    )
