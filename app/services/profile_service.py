from sqlalchemy.orm import Session
from app.models.memory import Memory
from app.services.llm_provider import ChatModel


def generate_user_profile(db: Session, user_id: str) -> str:
    """Generates a summarized user profile persona using an LLM based on user memories.

    Args:
        db (Session): SQLite database session.
        user_id (str): The identifier of the target user.

    Returns:
        str: Markdown formatted user profile.
    """
    memories = (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .all()
    )

    if not memories:
        return "No memories found for this user."

    memory_lines = [f"- [{m.category}] {m.content}" for m in memories]
    formatted_memories = "\n".join(memory_lines)

    prompt = f"""
You are an AI Persona Summarizer.

Based on the memories below, generate a markdown user profile summary.
Include sections for Key Skills, Preferences, and Important Notes.

User Memories:
{formatted_memories}
"""

    model = ChatModel()
    try:
        response = model.generate(prompt)
        return response
    except Exception as e:
        print(f"Error generating profile: {e}")
        return f"# User Profile: {user_id}\n\n" + formatted_memories