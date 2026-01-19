from fastapi import APIRouter
from models.schemas import CanvaReq
from services.pdf import html_to_pdf
from prompts.canva import prompt
from services.llm import ask

router = APIRouter()

@router.post("/doc")
def make_doc(req: CanvaReq):
    content = ask(prompt(req.title, req.content_hint))
    html = f"<h1>{req.title}</h1><pre>{content}</pre>"
    path = f"/tmp/{req.title.replace(' ','_')}.pdf"
    html_to_pdf(html, path)
    return {"pdf": path}
