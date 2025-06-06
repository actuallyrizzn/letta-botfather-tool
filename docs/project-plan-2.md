# Project Plan 2: Telethon Serialization Refactor

## Motivation

- Prevent all "database is locked" errors in Telethon-based services (BotFather Relay, Broca, etc.)
- Ensure robust, production-safe session management by serializing all Telethon access
- Establish a new project norm: **never run concurrent Telethon actions**

---

## Goals
- Refactor all Telethon-backed APIs to use a global request queue or lock
- Guarantee only one Telethon action runs at a time per process/account
- Document the new standard for all future development

---

## Affected Components
- BotFather Relay (FastAPI service)
- Developer onboarding docs

---

## Design Decisions
- Use a global `asyncio.Lock` or `asyncio.Queue` to serialize all Telethon operations
- All incoming HTTP/API requests must acquire the lock (or go through the queue) before calling any Telethon method
- No multi-worker or multi-process deployment for Telethon services (single-process async only)
- Document the rationale and pattern in code and onboarding

---

## Implementation Steps
1. **Audit** all Telethon usage in each service
2. **Add a global lock or queue** at the top of each service module
3. **Wrap all Telethon calls** (send, receive, etc.) in `async with lock:` or via a queue processor
4. **Update API endpoints** to acquire the lock before any Telethon interaction
5. **Add comments and docstrings** explaining the pattern and why it is required
6. **Update developer documentation** and onboarding guides

---

## Testing
- Unit tests: Ensure all Telethon calls are serialized (no concurrent access)
- Integration tests: Simulate multiple concurrent API requests and verify no "database is locked" errors occur
- Stress tests: High concurrency scenarios to confirm robustness

---

## Rollout Strategy
- Refactor and test in a feature branch
- Deploy to staging and run concurrency tests
- Roll out to production after validation
- Communicate the new standard to all developers

---

## Documentation
- Add a section to the README and onboarding docs:
  > "Never run concurrent Telethon actions. Always use a request queue or global lock."

---


## 🚨 Telethon API Concurrency Guard: Dev Instructions

### **DO THIS:**

**Guard all Telethon client actions with a global `asyncio.Lock`.**

**How:**

1. **In your `telethon_client.py` (or where you instantiate BotFatherSession):**

   ```python
   import asyncio
   telethon_lock = asyncio.Lock()
   ```

2. **Wrap every method that calls Telethon with:**

   ```python
   async with telethon_lock:
       # your Telethon code here
   ```

   Example:

   ```python
   async def send_message(self, entity: str, message: str) -> dict:
       async with telethon_lock:
           # ...existing Telethon logic...
   ```

3. **Apply this lock to ALL public methods that interact with Telethon’s client/session, including sending messages, fetching replies, etc.**

---

### **DO NOT:**

* ❌ Do **not** call Telethon client methods from more than one place at the same time **without** the lock.
* ❌ Do **not** attempt to “optimize” by removing the lock, batching, or using multiple locks.
* ❌ Do **not** run your server with Uvicorn’s `--reload` or with more than one worker.
* ❌ Do **not** create multiple `BotFatherSession`/Telethon client objects using the *same* session file.

---

### **Copy-Paste Example:**

```python
import asyncio
telethon_lock = asyncio.Lock()

class BotFatherSession:
    async def send_message(self, entity, message):
        async with telethon_lock:
            # Telethon send logic

    async def get_replies(self, entity, limit=3):
        async with telethon_lock:
            # Telethon reply logic
```

---

### **Summary**

* ✅ **ALWAYS** use a global `asyncio.Lock` to serialize access to Telethon.
* 🚫 **NEVER** access Telethon concurrently, use reload mode, or multi-worker HTTP.

This is **not optional**—Telethon + SQLite WILL break without it.
If you break these rules, you get to fix the bugs.
If you follow them, you’ll never see “database is locked” again.
