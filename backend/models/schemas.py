from pydantic import BaseModel
from typing import Optional, List


# -------------------------
# File schema (NEW)
# -------------------------
class FileItem(BaseModel):
    name: str
    text: str


# -------------------------
# Chat request / response
# -------------------------
class ChatReq(BaseModel):
    message: str
    mode: Optional[str] = "auto"  # auto|chat|live|dev|creative
    files: Optional[List[FileItem]] = None  # ✅ NEW (CRITICAL)


class ChatRes(BaseModel):
    reply: str


# -------------------------
# Canva (unchanged)
# -------------------------
class CanvaReq(BaseModel):
    title: str
    content_hint: str  # e.g., "Java interview notes"
