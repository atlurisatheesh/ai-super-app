from fastapi import APIRouter
from app.models.schemas import CanvaReq
from app.services.pdf import html_to_pdf
from app.prompts.canva import prompt
from app.services.llm import ask

router = APIRouter()

@router.post("/doc")
def make_doc(req: CanvaReq):
    content = ask(prompt(req.title, req.content_hint))
    html = f"<h1>{req.title}</h1><pre>{content}</pre>"
    path = f"/tmp/{req.title.replace(' ','_')}.pdf"
    html_to_pdf(html, path)
    return {"pdf": path}
