from fastapi import APIRouter
from models.schemas import ChatReq, ChatRes
from core.safety import legal
from core.router import run

router = APIRouter(prefix="/api/dev", tags=["Dev"])

@router.post("/", response_model=ChatRes)
def dev(req: ChatReq):
    if not legal(req.message):
        return ChatRes(reply="Cannot assist. Explaining concepts only.")

    return ChatRes(reply=run("dev", req.message))
