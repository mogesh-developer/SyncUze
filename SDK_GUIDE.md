# 🚀 SyncUze SDK Guide

The **SyncUze SDK** allows external Python projects (such as `SyncUze-Agent`, `SyncUze-Executor`, `SyncUze-Planner`, or custom services) to easily connect and interact with SyncUze.

---

## 📦 1. Installation in Other Projects

You can install `syncuze` directly into any other Python environment or project using `pip`:

### Option A: Install from Local Folder Path
```bash
pip install -e "path/to/SyncUze"
```

### Option B: Install from Git Repository
```bash
pip install git+https://github.com/mogesh-developer/SyncUze.git
```

### Option C: Add to `pyproject.toml` (Poetry)
```toml
[tool.poetry.dependencies]
syncuze = { path = "../SyncUze", develop = true }
```

---

## 💻 2. Usage Examples

### A. HTTP REST SDK Client (`MemoryClient`)
*Use this when SyncUze is running as a FastAPI microservice on `http://localhost:8000` or a remote server.*

```python
from syncuze import MemoryClient

# 1. Initialize Client
client = MemoryClient(base_url="http://localhost:8000")

# 2. Start a User Chat Session
session_info = client.start_session(user_id="mogesh")
session_id = session_info["session_id"]
print(f"Active Session: {session_id}")

# 3. Save User & Assistant Messages
client.save_memory(user_id="mogesh", role="user", text="I prefer dark mode in UI.", session_id=session_id)
client.save_memory(user_id="mogesh", role="assistant", text="Noted your preference!", session_id=session_id)

# 4. Perform Semantic Search
results = client.search_memory(user_id="mogesh", query="What UI theme does Mogesh like?")
print("Search Results:", results)

# 5. Fetch Profile & Timeline Summaries
profile = client.get_profile(user_id="mogesh")
print("User Profile:\n", profile["profile_summary"])

# 6. Interact via Chat with Context
reply = client.chat(user_id="mogesh", message="What are my saved preferences?")
print("Agent Reply:", reply["response"])
```

---

### B. Local Embedded SDK Client (`LocalMemoryClient`)
*Use this when your application runs in a single process and directly connects to the SQLite database without HTTP network latency.*

```python
from syncuze import LocalMemoryClient

client = LocalMemoryClient()

# Direct local database call
profile = client.get_profile(user_id="mogesh")
analytics = client.get_analytics(user_id="mogesh")
```

---

### C. Factory Function Initialization (`SyncUzeMemory`)
```python
from syncuze import SyncUzeMemory

# Returns MemoryClient (HTTP Mode)
memory_http = SyncUzeMemory(base_url="http://localhost:8000", mode="http")

# Returns LocalMemoryClient (Direct Mode)
memory_local = SyncUzeMemory(mode="local")
```

---

## 🛠️ 3. Full Method Reference

| Method | Return Type | Description |
| :--- | :--- | :--- |
| `start_session(user_id)` | `dict` | Starts or retrieves active session |
| `get_session(session_id)` | `list[dict]` | Returns session message logs |
| `save_memory(user_id, role, text, session_id=None)` | `dict` | Saves interaction log |
| `get_history(user_id)` | `list[dict]` | Returns all raw interaction logs |
| `get_all_memories(user_id)` | `list[dict]` | Returns all stored memory entries |
| `search_memory(user_id, query)` | `dict` | Semantic similarity vector search |
| `get_profile(user_id)` | `dict` | Persona markdown summary |
| `get_timeline(user_id)` | `dict` | Milestone graph timeline |
| `get_analytics(user_id)` | `dict` | Category breakdowns and stats |
| `cleanup_memories(days=30, importance_limit=3)` | `dict` | Forgetting engine purging |
| `chat(user_id, message)` | `dict` | Contextual chat response |
| `extract_memories(session_id)` | `list[dict]` | Extract facts from session |
