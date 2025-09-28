from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from database import get_db
from models.ai_chat_session import AIChatSession
from models.reported_cases import ReportedCases
from schemas.ai_chat import (
    ChatSessionCreate, ChatSessionResponse, ChatMessageRequest, 
    ChatMessageResponse, CaseSummaryRequest, CaseSummaryResponse,
    ChatSessionListResponse, ChatMessage
)
from services.ai_chat_service import AIChatService

router = APIRouter(prefix="/ai-chat", tags=["ai-chat"])

@router.post("/sessions", response_model=ChatSessionResponse)
async def create_chat_session(
    session_data: ChatSessionCreate,
    db: Session = Depends(get_db)
    # Temporarily disabled authentication for testing
    # current_user = Depends(get_current_user)
):
    """Create a new AI chat session for a case"""
    try:
        # Verify case exists
        case = db.query(ReportedCases).filter(ReportedCases.id == session_data.case_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Create new session
        session_id = str(uuid.uuid4())
        new_session = AIChatSession(
            session_id=session_id,
            case_id=session_data.case_id,
            user_id=session_data.user_id,
            title=session_data.title or f"Chat for {case.title[:50]}...",
            is_active=True,
            messages=[],
            total_messages=0,
            ai_model_used="gpt-4"
        )
        
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        
        return new_session
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating chat session: {str(e)}")

@router.get("/sessions", response_model=ChatSessionListResponse)
async def get_chat_sessions(
    case_id: Optional[int] = Query(None, description="Filter by case ID"),
    user_id: Optional[int] = Query(None, description="Filter by user ID"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(20, ge=1, le=100, description="Items per page"),
    db: Session = Depends(get_db)
):
    """Get chat sessions with optional filtering"""
    try:
        query = db.query(AIChatSession).filter(AIChatSession.is_active == True)
        
        if case_id:
            query = query.filter(AIChatSession.case_id == case_id)
        if user_id:
            query = query.filter(AIChatSession.user_id == user_id)
        
        # Get total count
        total = query.count()
        
        # Apply pagination
        offset = (page - 1) * limit
        sessions = query.order_by(AIChatSession.last_activity.desc()).offset(offset).limit(limit).all()
        
        # Convert to response format
        session_responses = []
        for session in sessions:
            messages = []
            if session.messages:
                for msg in session.messages:
                    messages.append(ChatMessage(
                        role=msg.get("role", "user"),
                        content=msg.get("content", ""),
                        timestamp=datetime.fromisoformat(msg.get("timestamp", datetime.utcnow().isoformat()))
                    ))
            
            session_responses.append(ChatSessionResponse(
                id=session.id,
                session_id=session.session_id,
                case_id=session.case_id,
                user_id=session.user_id,
                title=session.title,
                is_active=session.is_active,
                total_messages=session.total_messages,
                created_at=session.created_at,
                updated_at=session.updated_at,
                last_activity=session.last_activity,
                messages=messages
            ))
        
        total_pages = (total + limit - 1) // limit
        
        return ChatSessionListResponse(
            sessions=session_responses,
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat sessions: {str(e)}")

@router.get("/sessions/{session_id}", response_model=ChatSessionResponse)
async def get_chat_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific chat session by ID"""
    try:
        session = db.query(AIChatSession).filter(
            AIChatSession.session_id == session_id,
            AIChatSession.is_active == True
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Convert messages
        messages = []
        if session.messages:
            for msg in session.messages:
                messages.append(ChatMessage(
                    role=msg.get("role", "user"),
                    content=msg.get("content", ""),
                    timestamp=datetime.fromisoformat(msg.get("timestamp", datetime.utcnow().isoformat()))
                ))
        
        return ChatSessionResponse(
            id=session.id,
            session_id=session.session_id,
            case_id=session.case_id,
            user_id=session.user_id,
            title=session.title,
            is_active=session.is_active,
            total_messages=session.total_messages,
            created_at=session.created_at,
            updated_at=session.updated_at,
            last_activity=session.last_activity,
            messages=messages
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching chat session: {str(e)}")

@router.post("/sessions/{session_id}/messages", response_model=ChatMessageResponse)
async def send_message(
    session_id: str,
    message_data: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """Send a message to an AI chat session"""
    try:
        # Get session
        session = db.query(AIChatSession).filter(
            AIChatSession.session_id == session_id,
            AIChatSession.is_active == True
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Initialize AI service
        ai_service = AIChatService(db)
        
        # Get chat history
        chat_history = session.messages or []
        
        # Generate AI response
        ai_response = ai_service.generate_ai_response(
            case_id=session.case_id,
            user_message=message_data.message,
            chat_history=chat_history
        )
        
        if not ai_response.get("success", False):
            raise HTTPException(
                status_code=500, 
                detail=f"AI service error: {ai_response.get('error', 'Unknown error')}"
            )
        
        # Create message objects
        user_message = {
            "role": "user",
            "content": message_data.message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        ai_message = {
            "role": "assistant",
            "content": ai_response["response"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Update session with new messages
        session.messages = chat_history + [user_message, ai_message]
        session.total_messages = len(session.messages)
        session.last_activity = datetime.utcnow()
        
        db.commit()
        
        return ChatMessageResponse(
            success=True,
            message=ChatMessage(
                role="assistant",
                content=ai_response["response"],
                timestamp=datetime.fromisoformat(ai_message["timestamp"])
            ),
            session_id=session_id,
            case_context=ai_response.get("case_context")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error sending message: {str(e)}")

@router.post("/sessions/{case_id}/start", response_model=ChatMessageResponse)
async def start_new_chat(
    case_id: int,
    message_data: ChatMessageRequest,
    db: Session = Depends(get_db)
):
    """Start a new chat session and send the first message"""
    try:
        # Verify case exists
        case = db.query(ReportedCases).filter(ReportedCases.id == case_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Create new session
        session_id = str(uuid.uuid4())
        new_session = AIChatSession(
            session_id=session_id,
            case_id=case_id,
            user_id=None,  # No authentication for now
            title=f"Chat for {case.title[:50]}...",
            is_active=True,
            messages=[],
            total_messages=0,
            ai_model_used="gpt-4"
        )
        
        db.add(new_session)
        db.commit()
        db.refresh(new_session)
        
        # Initialize AI service
        ai_service = AIChatService(db)
        
        # Generate AI response
        ai_response = ai_service.generate_ai_response(
            case_id=case_id,
            user_message=message_data.message,
            chat_history=[]
        )
        
        if not ai_response.get("success", False):
            raise HTTPException(
                status_code=500, 
                detail=f"AI service error: {ai_response.get('error', 'Unknown error')}"
            )
        
        # Create message objects
        user_message = {
            "role": "user",
            "content": message_data.message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        ai_message = {
            "role": "assistant",
            "content": ai_response["response"],
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Update session with messages
        new_session.messages = [user_message, ai_message]
        new_session.total_messages = 2
        new_session.last_activity = datetime.utcnow()
        
        db.commit()
        
        return ChatMessageResponse(
            success=True,
            message=ChatMessage(
                role="assistant",
                content=ai_response["response"],
                timestamp=datetime.fromisoformat(ai_message["timestamp"])
            ),
            session_id=session_id,
            case_context=ai_response.get("case_context")
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error starting new chat: {str(e)}")

@router.post("/case-summary", response_model=CaseSummaryResponse)
async def generate_case_summary(
    summary_data: CaseSummaryRequest,
    db: Session = Depends(get_db)
):
    """Generate a comprehensive AI summary of a case"""
    try:
        # Verify case exists
        case = db.query(ReportedCases).filter(ReportedCases.id == summary_data.case_id).first()
        if not case:
            raise HTTPException(status_code=404, detail="Case not found")
        
        # Initialize AI service
        ai_service = AIChatService(db)
        
        # Generate summary
        summary_result = ai_service.generate_case_summary(summary_data.case_id)
        
        if not summary_result.get("success", False):
            raise HTTPException(
                status_code=500, 
                detail=f"AI service error: {summary_result.get('error', 'Unknown error')}"
            )
        
        return CaseSummaryResponse(
            success=True,
            summary=summary_result["summary"],
            timestamp=datetime.fromisoformat(summary_result["timestamp"])
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating case summary: {str(e)}")

@router.delete("/sessions/{session_id}")
async def delete_chat_session(
    session_id: str,
    db: Session = Depends(get_db)
):
    """Delete a chat session (soft delete)"""
    try:
        session = db.query(AIChatSession).filter(
            AIChatSession.session_id == session_id,
            AIChatSession.is_active == True
        ).first()
        
        if not session:
            raise HTTPException(status_code=404, detail="Chat session not found")
        
        # Soft delete
        session.is_active = False
        session.updated_at = datetime.utcnow()
        
        db.commit()
        
        return {"success": True, "message": "Chat session deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error deleting chat session: {str(e)}")

