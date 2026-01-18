# ai-super-app

pip install fastapi uvicorn openai weasyprint python-dotenv
uvicorn app.main:app --reload

uvicorn app.main:app --reload

# AI Super App

An AI-powered super application with:
- Chat
- Dev debugging
- Image generation
- File upload
- Streaming responses

## Tech Stack
- Next.js (Frontend)
- FastAPI (Backend)
- Supabase
- OpenAI-compatible LLMs

## Setup

### Frontend
```bash
cd frontend
npm install
npm run dev
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
