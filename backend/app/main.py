# backend/app/main.py
from fastapi import FastAPI
from .db import create_db_and_tables
from .routers import chat
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AgriCopilot (Text-only)")
app.include_router(chat.router)

# Allow frontend (Next.js) to call the backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # you can restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],  # allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "LLaMA API is running 🚀"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/health")
def health():
    return {"status":"ok"}
