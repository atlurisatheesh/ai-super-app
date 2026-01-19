from fastapi import APIRouter
from fastapi.responses import StreamingResponse


from core.intent import intent
from core.router import run, run_stream
from models.schemas import ChatReq, ChatRes

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
    mode = intent(req.message)

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

    return ChatRes(
        reply=run(mode, final_message)
    )


# @router.post("/stream")
# def chat_stream(req: ChatReq):
#     mode = intent(req.message)

#     file_context = build_file_context(
#         getattr(req, "files", None)
#     )

#     final_message = (
#         f"You are an assistant with access to the following documents:\n\n"
#         f"{file_context}\n"
#         f"User message:\n{req.message}"
#         if file_context
#         else req.message
#     )

#     return StreamingResponse(
#         run_stream(mode, final_message),
#         media_type="text/plain"
#     )



@router.post("/stream")
def chat_stream(req: ChatReq):
    try:
        mode = intent(req.message)

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

        return StreamingResponse(
            run_stream(mode, final_message),
            media_type="text/plain"
        )

    except Exception as e:
        print("❌ STREAM ERROR:", repr(e))
        raise
