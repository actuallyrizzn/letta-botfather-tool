## **BotFather CLI Refactor Plan**

### **Objective**

Refactor the existing BotFather API relay into a **single, modular command-line tool** that:

* Preserves all existing features (message send, reply fetch, authentication, etc.)
* Has no API/web server
* Is cleanly structured for future extension
* Is robust for one-off use (no concurrency)

---

### **Steps for Devs**

#### **1. Strip FastAPI and API Routing**

* Remove all FastAPI and Uvicorn code.
* Eliminate any web server logic, routes, and dependency injection.

#### **2. Select CLI Framework**

* Use `argparse` (standard library, preferred for this project).
* The CLI should provide subcommands for every current API endpoint, e.g.:

  * `send-message`
  * `get-replies`
  * `authenticate` (if not automatic)
  * Any other core operations

#### **3. Refactor Core Logic**

* Move business logic (currently in routers/controllers) into Python functions or modules.
* Each subcommand in the CLI calls these functions directly, passing command-line args.

#### **4. Modular Structure**

* Organize code by actions, e.g.:

  * `actions/send_message.py`
  * `actions/get_replies.py`
  * etc.
* Keep `telethon_client.py` as the abstraction for all Telegram interactions.

#### **5. Session Handling**

* Session file remains persistent in a configurable location (default: project root).
* If session is missing, tool prompts for login/OTP as before.

#### **6. Error Handling & Output**

* Print result of each action to `stdout`.
* Print user-friendly errors to `stderr` and use appropriate non-zero exit codes for failures.

#### **7. Help & Documentation**

* Implement `--help` for the CLI and for each subcommand.
* Include sample usages in `README.md`.

#### **8. Minimal Dependencies**

* `telethon`
* Anything else strictly required by the logic

#### **9. Test Each Action Standalone**

* Validate every action via CLI:

  * `python botfather_cli.py send-message --to @user --msg "hi"`
  * `python botfather_cli.py get-replies --entity @user --limit 5`
* Confirm *no* API server starts; *no* concurrency bugs occur.

#### **10. Document for MCP Integration**

* Note expected arguments and outputs for future MCP wrapper.

---

### **Sample CLI Structure (Pseudocode)**

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="BotFather CLI tool")
    subparsers = parser.add_subparsers(dest="command")

    send_parser = subparsers.add_parser("send-message")
    send_parser.add_argument("--to", required=True)
    send_parser.add_argument("--msg", required=True)

    get_parser = subparsers.add_parser("get-replies")
    get_parser.add_argument("--entity", required=True)
    get_parser.add_argument("--limit", type=int, default=3)

    args = parser.parse_args()

    if args.command == "send-message":
        # Call Telethon logic to send message
        pass
    elif args.command == "get-replies":
        # Call Telethon logic to get replies
        pass
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
```

---

### **Delivery Checklist**

* [ ] All current API actions available as CLI commands
* [ ] No web server or FastAPI code remains
* [ ] Modular, readable, and easily extensible structure
* [ ] Clear documentation and `--help`
* [ ] Easy to wrap in MCP or call from scripts

---

**Add to README:**

* “This CLI is meant to be called directly or via a local MCP server.
* Never run more than one at a time.
* For all new actions, add as a new CLI subcommand and update help.”

