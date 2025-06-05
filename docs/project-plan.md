# 🛠️ **Project Plan: Telegram BotFather Provisioning System** (Revised for Dev Swarm)

## 🔥 Project Overview

We’re building a **two-part system** that enables Monday (Sanctum agent) to provision Telegram bots via BotFather using an external relay. This design decouples the Telegram interactions from the Sanctum container and makes the system flexible, testable, and future-proof.

---

## 🚧 **Part One: Local BotFather API Relay**

### 📍 **Purpose**

* Provide a local relay between Monday and BotFather using Telethon.
* Expose a local HTTP API (FastAPI) for sending messages to BotFather and retrieving replies.
* Runs on the same machine as Letta/Sanctum (don’t ask where—if you can’t find it, maybe you shouldn’t be on the swarm).

### 📍 **Key Features**

✅ Telethon connection using Monday’s credentials—no excuses if you mess it up.
✅ Accepts HTTP POST requests with a message to send to BotFather.
✅ Forwards message and retrieves the latest replies (use your brain on parsing).
✅ Returns JSON. If you can’t format JSON, maybe pick another profession.
✅ Runs in `screen` or `tmux`—don’t complain if you can’t figure that out.

### 📍 **Deliverables**

* **`botfather_relay.py`**

  * **Telethon Initialization:** Establish a session using Monday’s credentials.
  * **FastAPI Server:** Listens on `localhost:57431` (not 8000).
  * **Endpoint `/send_message`:**

    * Accepts JSON: `{ "message": "<text to send to BotFather>" }`
    * Forwards the message to BotFather.
    * Retrieves and returns the 3 most recent replies in JSON: `{ "messages": [ ... ] }`
    * Returns structured error JSON on failure.
  * **Session Management:** Handle login/logout securely.
  * **Logging:** INFO-level, with timestamps; never log tokens.
  * **Error Handling:** Connectivity issues, timeouts, invalid input; returns errors to the client.
  * **Comments:** Descriptive and useful throughout the code.

* **`README.md`**

  * **Setup Instructions:**

    * How to obtain and configure API ID, hash, phone number.
    * How to run in `screen`/`tmux`.
  * **Usage Guide:**

    * Example request and response for `/send_message`.
    * Explanation of the JSON response structure and error format.
  * **Security Notes:**

    * API runs on `localhost` ONLY.
    * Recommendation to add a bearer token for extra auth.
  * **Troubleshooting:**

    * Common issues, fixes, and debugging tips.

---

## 🚧 **Part Two: Tool Function for Testing & Integration**

### 📍 **Purpose**

* Provide a self-contained function or script to talk to the relay.
* Tool module for Monday’s framework.
* CLI tool so even the laziest dev can test it manually.

### 📍 **Key Features**

✅ Python function: `provision_botfather_message(message: str) -> List[str]`.
✅ No dependencies beyond Python standard library and `requests`—don’t break the rules.
✅ CLI interface:

```bash
python botfather.py "/newbot"
```

✅ Comments that explain what you’re doing. Comments that *actually* help the next person.

### 📍 **Deliverables**

* **`botfather.py`**

  * Python module with a function: `provision_botfather_message(message: str) -> List[str]`

    * Sends a POST request to the relay at `http://localhost:57431/send_message`.
    * Returns a list of BotFather replies.
  * CLI entry point using `argparse`, enabling usage like:

    ```
    python botfather.py "/newbot"
    ```
  * Only Python standard library + `requests` allowed.
  * Clear, descriptive comments and docstrings throughout.
  * CLI prints BotFather responses in a human-readable way.

* **Integration Instructions**

  * Markdown snippet for the README demonstrating usage and expected responses for both the function and CLI.

* **Test Script (optional but recommended)**

  * Minimal Python test script covering typical use and error cases.

---

## 🗂️ **Project Structure**

```
project_root/
  ├── botfather_relay.py
  ├── botfather.py
  └── README.md
```

---

## 🔒 **Security Considerations**

* Bind to localhost (`127.0.0.1`).
* Optional: Add token auth if you can handle it.
* No logging of tokens—duh.

---

## 📝 **Testing & Validation**

* **Unit tests:** Automated tests for both `botfather.py` and `botfather_relay.py` (including edge cases and error handling).
* **Integration tests:** Simulate end-to-end flows between the relay and tool, verifying actual message passing and error scenarios.
* **Manual testing by user:**

  * Run CLI:

    * `python botfather.py "/newbot"`
  * Simulated testing via Monday’s framework.
  * Full end-to-end validation with real Telegram credentials and BotFather.
