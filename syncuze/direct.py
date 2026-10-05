from typing import Any, Dict, List, Optional


class LocalMemoryClient:
    """Embedded Python SDK client for direct database interaction without HTTP network calls."""

    @staticmethod
    def chat(user_id: str, message: str) -> Dict[str, Any]:
        """Sends a message to the memory engine and returns context-aware response."""
        from app.database import SessionLocal
        from app.services.chat_service import chat as chat_func

        db = SessionLocal()
        try:
            res = chat_func(db, user_id, message)
            return {"user_id": user_id, "message": message, "response": res}
        finally:
            db.close()

    @staticmethod
    def get_profile(user_id: str) -> Dict[str, Any]:
        """Retrieves summarized user profile persona markdown."""
        from app.database import SessionLocal
        from app.services.profile_service import generate_user_profile

        db = SessionLocal()
        try:
            summary = generate_user_profile(db, user_id)
            return {"user_id": user_id, "profile_summary": summary}
        finally:
            db.close()

    @staticmethod
    def get_timeline(user_id: str) -> Dict[str, Any]:
        """Retrieves chronological timeline milestone summary graph."""
        from app.database import SessionLocal
        from app.services.timeline_service import generate_user_timeline

        db = SessionLocal()
        try:
            timeline = generate_user_timeline(db, user_id)
            return {"user_id": user_id, "timeline": timeline}
        finally:
            db.close()

    @staticmethod
    def get_analytics(user_id: str) -> Dict[str, Any]:
        """Retrieves database counts and category breakdowns."""
        from app.database import SessionLocal
        from app.services.analytics_service import get_user_analytics

        db = SessionLocal()
        try:
            stats = get_user_analytics(db, user_id)
            return {"user_id": user_id, "analytics": stats}
        finally:
            db.close()

    @staticmethod
    def search_memory(user_id: str, query: str) -> Dict[str, Any]:
        """Searches memories using vector similarity."""
        from app.services.memory_service import search_memories

        return search_memories(user_id, query)

    @staticmethod
    def save_memory(
        user_id: str,
        role: str,
        text: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Saves a message interaction into local storage."""
        from app.database import SessionLocal
        from app.schemas.message import MessageCreate
        from app.services.memory_service import save_memory as save_func

        db = SessionLocal()
        try:
            msg_create = MessageCreate(user_id=user_id, role=role, text=text, session_id=session_id)
            saved = save_func(db, msg_create)
            return {"status": "success", "id": saved.id}
        finally:
            db.close()

    @staticmethod
    def get_history(user_id: str) -> List[Dict[str, Any]]:
        """Retrieves raw history of messages."""
        from app.database import SessionLocal
        from app.services.memory_service import get_history as get_hist_func

        db = SessionLocal()
        try:
            messages = get_hist_func(db, user_id)
            return [
                {
                    "id": m.id,
                    "user_id": m.user_id,
                    "role": m.role,
                    "text": m.text,
                    "session_id": m.session_id,
                    "timestamp": str(m.timestamp) if hasattr(m, "timestamp") else None,
                }
                for m in messages
            ]
        finally:
            db.close()

    @staticmethod
    def cleanup_memories(days: int = 30, importance_limit: int = 3) -> Dict[str, Any]:
        """Purges old low-importance memories."""
        from app.database import SessionLocal
        from app.services.forgetting_service import run_forgetting_engine

        db = SessionLocal()
        try:
            deleted_count = run_forgetting_engine(db, days_threshold=days, importance_limit=importance_limit)
            return {"status": "success", "forgotten_memories_count": deleted_count}
        finally:
            db.close()
