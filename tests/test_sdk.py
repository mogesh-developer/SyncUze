from unittest.mock import patch, MagicMock
import pytest
from syncuze import MemoryClient, LocalMemoryClient, SyncUzeMemory


def test_syncuze_memory_factory():
    client_http = SyncUzeMemory(mode="http", base_url="http://localhost:8000")
    assert isinstance(client_http, MemoryClient)
    assert client_http.base_url == "http://localhost:8000"

    client_local = SyncUzeMemory(mode="local")
    assert isinstance(client_local, LocalMemoryClient)


@patch("requests.post")
def test_memory_client_start_session(mock_post):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"status": "success", "session_id": "test-session-123", "user_id": "user1"}
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp

    client = MemoryClient("http://localhost:8000")
    res = client.start_session("user1")

    assert res["session_id"] == "test-session-123"
    mock_post.assert_called_once_with(
        "http://localhost:8000/session/start",
        json={"user_id": "user1"},
        timeout=30.0
    )


@patch("requests.post")
def test_memory_client_save_memory(mock_post):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"status": "success", "id": 1}
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp

    client = MemoryClient("http://localhost:8000")
    res = client.save_memory("user1", "user", "Hello SDK", session_id="s1")

    assert res["status"] == "success"
    assert res["id"] == 1
    mock_post.assert_called_once_with(
        "http://localhost:8000/memory/save",
        json={"user_id": "user1", "role": "user", "text": "Hello SDK", "session_id": "s1"},
        timeout=30.0
    )


@patch("requests.get")
def test_memory_client_get_history(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = [{"role": "user", "text": "Hello SDK"}]
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    client = MemoryClient("http://localhost:8000")
    res = client.get_history("user1")

    assert len(res) == 1
    assert res[0]["text"] == "Hello SDK"
    mock_get.assert_called_once_with(
        "http://localhost:8000/memory/history/user1",
        timeout=30.0
    )


@patch("requests.get")
def test_memory_client_get_profile(mock_get):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"user_id": "user1", "profile_summary": "Summary Profile"}
    mock_resp.raise_for_status.return_value = None
    mock_get.return_value = mock_resp

    client = MemoryClient("http://localhost:8000")
    res = client.get_profile("user1")

    assert res["profile_summary"] == "Summary Profile"
    mock_get.assert_called_once_with(
        "http://localhost:8000/memory/profile/user1",
        timeout=30.0
    )


@patch("requests.post")
def test_memory_client_cleanup(mock_post):
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"status": "success", "forgotten_memories_count": 5}
    mock_resp.raise_for_status.return_value = None
    mock_post.return_value = mock_resp

    client = MemoryClient("http://localhost:8000")
    res = client.cleanup_memories(days=30, importance_limit=2)

    assert res["forgotten_memories_count"] == 5
    mock_post.assert_called_once_with(
        "http://localhost:8000/memory/cleanup",
        params={"days": 30, "importance_limit": 2},
        timeout=30.0
    )


def test_local_memory_client(db_session):
    client = LocalMemoryClient()
    saved = client.save_memory("local_user", "user", "Local SDK Test", "sess_local")
    assert saved["status"] == "success"

    hist = client.get_history("local_user")
    assert len(hist) >= 1
    assert hist[0]["text"] == "Local SDK Test"
