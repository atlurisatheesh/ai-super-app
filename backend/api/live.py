from fastapi import APIRouter
from app.models.schemas import ChatReq, ChatRes
from app.core.safety import legal
from app.core.router import run

router = APIRouter(prefix="/api/live", tags=["Live"])


@router.post("/", response_model=ChatRes)
def live(req: ChatReq):
    if not legal(req.message):
        return ChatRes(reply="Safe guidance only.")
    return ChatRes(reply=run("live", req.message))
