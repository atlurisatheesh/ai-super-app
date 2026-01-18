from fastapi import APIRouter
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter(
    prefix="/image",
    tags=["image"]
)

client = OpenAI()

class ImageRequest(BaseModel):
    prompt: str

@router.post("")
def generate_image(req: ImageRequest):
    """
    Generate an image from a text prompt
    """
    result = client.images.generate(
        model="gpt-image-1",
        prompt=req.prompt,
        size="1024x1024"
    )

    return {
        "url": result.data[0].url
    }
