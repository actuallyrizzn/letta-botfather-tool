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
   git clone https://github.com/yourusername/letta-botfather-tool.git
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

All actions are performed via the CLI tool:

### Send a message to BotFather
```bash
python botfather_cli.py send-message --to BotFather --msg "/newbot"
```

### Get replies from BotFather
```bash
python botfather_cli.py get-replies --entity BotFather --limit 3
```

- The tool will prompt for authentication if the session is missing or expired.
- All output is printed to stdout; errors to stderr.

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
