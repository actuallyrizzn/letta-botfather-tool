# 🛠️ BotFather CLI Tool

A robust, modular command-line tool for provisioning and managing Telegram bots via BotFather. This tool uses Telethon for all Telegram interactions and is designed for one-off, non-concurrent use—no web server, no API, no concurrency bugs.

## 🚀 Features

- 📬 Send messages and commands to BotFather from the CLI
- 🔄 Automatic session management and authentication
- 📝 Clear, user-friendly CLI output and error handling
- 🛡️ No concurrency: safe, predictable, and production-ready
- 🧩 Easily extensible for new actions and MCP integration

## 📋 Prerequisites

- Python 3.8 or higher
- Telegram API credentials (API ID and API Hash)
- Telegram account with phone number

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/actuallyrizzn/letta-botfather-tool.git
   cd letta-botfather-tool
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Unix/MacOS:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```env
   TELEGRAM_API_ID=your_api_id
   TELEGRAM_API_HASH=your_api_hash
   TELEGRAM_PHONE=your_phone_number
   # Optionally: TELETHON_SESSION_NAME=botfather_session
   ```

## 🚀 Usage

All actions are performed via the CLI tool. **All commands implicitly target BotFather.**

### Basic Commands

#### Send a message to BotFather
```bash
python botfather_cli.py send-message --msg "/newbot"
```

#### Get replies from BotFather
```bash
python botfather_cli.py get-replies --limit 3
```

#### Click a button in BotFather's message
```bash
# Click by button text (case-insensitive, @ prefix optional)
python botfather_cli.py click-button --button-text "Payments"
python botfather_cli.py click-button --button-text "@Payments"

# Click by position (0-based indices)
python botfather_cli.py click-button --row 1 --col 1

# Optional: specify message ID (defaults to last message)
python botfather_cli.py click-button --msg-id 123 --button-text "Payments"
```

### Command Reference

#### `send-message`
Sends a message to BotFather.

Required arguments:
- `--msg`: The message to send

Example:
```bash
python botfather_cli.py send-message --msg "/newbot"
```

#### `get-replies`
Gets the last N messages from BotFather.

Optional arguments:
- `--limit`: Number of messages to retrieve (default: 1)

Example:
```bash
python botfather_cli.py get-replies --limit 3
```

#### `click-button`
Clicks a button in a BotFather message.

Required arguments (one of):
- `--button-text`: Text of the button to click (case-insensitive, @ prefix optional)
- `--row` and `--col`: Position of the button (0-based indices)

Optional arguments:
- `--msg-id`: ID of the message containing the button (defaults to last message)

Examples:
```bash
# Click by text
python botfather_cli.py click-button --button-text "Payments"
python botfather_cli.py click-button --button-text "@Payments"

# Click by position
python botfather_cli.py click-button --row 1 --col 1

# Click in specific message
python botfather_cli.py click-button --msg-id 123 --button-text "Payments"
```

### Output Format

All commands return JSON-formatted output:

#### `send-message` output:
```json
{
    "id": 123,
    "text": "Message text"
}
```

#### `get-replies` output:
```json
[
    {
        "id": 123,
        "text": "Message text",
        "buttons": [
            ["Button 1", "Button 2"],
            ["Button 3"]
        ]
    }
]
```

#### `click-button` output:
```json
{
    "id": 123,
    "button": "Button text or (row, col)",
    "result": "Result of button click",
    "status": "success or error"
}
```

## 🗂️ Project Structure
```
project_root/
  ├── botfather_cli.py           # Main CLI entry point
  ├── telethon_client.py         # Telethon logic abstraction
  ├── config.py                  # Telegram API credentials/config
  ├── README.md                  # This file
  ├── CHANGELOG.md               # Project history
  ├── requirements.txt           # Python dependencies
  ├── LICENSE                    # License
  ├── docs/                      # Project plans and notes
  └── ... (session files, etc.)
```

## 📝 Session Handling
- The tool stores your Telegram session in the project root (or as configured).
- If the session is missing, you will be prompted for a login code and (if needed) 2FA password.
- **Never run more than one instance at a time.**

## 🛡️ Concurrency & Safety
- All Telethon access is serialized with a global lock.
- No concurrency, no web server, no "database is locked" errors.
- Designed for robust, one-off CLI use and easy MCP integration.

## 🤝 Contributing
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License.

## ⚠️ Disclaimer

This tool is part of the larger Sanctum toolset and is designed for use with Letta agents. Use responsibly and in accordance with Telegram's terms of service.
