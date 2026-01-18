from fastapi import APIRouter
from app.models.schemas import ChatReq, ChatRes
from app.core.safety import legal
from app.core.router import run

router = APIRouter(prefix="/api/creative", tags=["Creative"])



@router.post("/", response_model=ChatRes)
def creative(req: ChatReq):
    if not legal(req.message):
        return ChatRes(reply="Safe content only.")
    return ChatRes(reply=run("creative", req.message))
