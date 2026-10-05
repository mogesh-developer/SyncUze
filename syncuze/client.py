from typing import Any, Dict, List, Optional
import requests


class MemoryClient:
    """HTTP Client for communicating with the SyncUze FastAPI service."""

    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def start_session(self, user_id: str) -> Dict[str, Any]:
        """Starts a new chat session or returns an active session for the given user."""
        url = f"{self.base_url}/session/start"
        res = requests.post(url, json={"user_id": user_id}, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def get_session(self, session_id: str) -> List[Dict[str, Any]]:
        """Retrieves chronological messages for a specific session ID."""
        url = f"{self.base_url}/session/{session_id}"
        res = requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def save_memory(
        self,
        user_id: str,
        role: str,
        text: str,
        session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Saves a message interaction for a user into memory history."""
        url = f"{self.base_url}/memory/save"
        payload = {
            "user_id": user_id,
            "role": role,
            "text": text,
        }
        if session_id:
            payload["session_id"] = session_id
        res = requests.post(url, json=payload, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetches all raw user message interaction logs across sessions."""
        url = f"{self.base_url}/memory/history/{user_id}"
        res = requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def get_all_memories(self, user_id: str) -> List[Dict[str, Any]]:
        """Fetches all processed memories stored for a user."""
        url = f"{self.base_url}/memory/all/{user_id}"
        res = requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def search_memory(self, user_id: str, query: str) -> Dict[str, Any]:
        """Performs semantic vector search across user memories."""
        url = f"{self.base_url}/memory/search"
        res = requests.post(url, json={"user_id": user_id, "query": query}, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def get_profile(self, user_id: str) -> Dict[str, Any]:
        """Generates and returns the user persona summary markdown."""
        url = f"{self.base_url}/memory/profile/{user_id}"
        res = requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def get_timeline(self, user_id: str) -> Dict[str, Any]:
        """Generates visual milestone graph timeline for a user."""
        url = f"{self.base_url}/memory/timeline/{user_id}"
        res = requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def get_analytics(self, user_id: str) -> Dict[str, Any]:
        """Returns database counts, category breakdowns, and memory stats."""
        url = f"{self.base_url}/memory/analytics/{user_id}"
        res = requests.get(url, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def cleanup_memories(self, days: int = 30, importance_limit: int = 3) -> Dict[str, Any]:
        """Runs forgetting engine to purge old low-importance memories."""
        url = f"{self.base_url}/memory/cleanup"
        params = {"days": days, "importance_limit": importance_limit}
        res = requests.post(url, params=params, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def chat(self, user_id: str, message: str) -> Dict[str, Any]:
        """Sends a chat message to the agent, incorporating memory context."""
        url = f"{self.base_url}/chat"
        res = requests.post(url, json={"user_id": user_id, "message": message}, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def extract_memories(self, session_id: str) -> List[Dict[str, Any]]:
        """Extracts structured memories from a completed chat session."""
        url = f"{self.base_url}/memory/extract/{session_id}"
        res = requests.post(url, timeout=self.timeout)
        res.raise_for_status()
        return res.json()

    def backfill_embeddings(self, user_id: str) -> Dict[str, Any]:
        """Backfills embeddings for unindexed user memories."""
        url = f"{self.base_url}/memory/embed/{user_id}"
        res = requests.post(url, timeout=self.timeout)
        res.raise_for_status()
        return res.json()
