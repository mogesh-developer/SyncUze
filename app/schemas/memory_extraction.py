from typing import List, Optional
from pydantic import BaseModel


class MemoryExtractionItem(BaseModel):
    category: str
    content: str


class MemoryExtractionResponse(BaseModel):
    memories: List[MemoryExtractionItem]


class MemoryConflictCheck(BaseModel):
    updates_id: Optional[int] = None
    merged_content: Optional[str] = None
