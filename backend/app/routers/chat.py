from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional
from ..db import get_session
from ..models import User, ChatMessage
from ..services.llama_service import generate_text
from ..services.weather_service import get_weather
from ..services.market_service import get_mandi_price

router = APIRouter()

# ----------------------------
# Request/Response Schemas
# ----------------------------
class ChatRequest(BaseModel):
    user_id: Optional[int] = None
    message: str
    phone: Optional[str] = None
    location: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    user_id: int

class GenerateRequest(BaseModel):
    prompt: str

class GenerateResponse(BaseModel):
    response: str

# ----------------------------
# Chat Endpoint
# ----------------------------
@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, session: Session = Depends(get_session)):
    # Get or create user
    user = None
    if request.user_id:
        user = session.get(User, request.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
    elif request.phone:
        # Try to find user by phone
        user = session.exec(select(User).where(User.phone == request.phone)).first()
        if not user:
            # Create new user
            user = User(phone=request.phone, location=request.location)
            session.add(user)
            session.commit()
            session.refresh(user)
    else:
        raise HTTPException(status_code=400, detail="Either user_id or phone must be provided")
    
    # Save user message
    user_message = ChatMessage(user_id=user.id, role="user", content=request.message)
    session.add(user_message)
    session.commit()
    
    # Generate response from LLaMA
    response = await generate_text(request.message)
    
    # Save assistant message
    assistant_message = ChatMessage(user_id=user.id, role="assistant", content=response)
    session.add(assistant_message)
    session.commit()
    
    return ChatResponse(response=response, user_id=user.id)

# ----------------------------
# Simple Text Generation Endpoint
# ----------------------------
# Text generation with request body
@router.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest = None, prompt: str = None):
    # Handle both request formats
    text_to_generate = prompt
    if request and hasattr(request, 'prompt'):
        text_to_generate = request.prompt
        
    response = await generate_text(text_to_generate)
    return {"response": response}
