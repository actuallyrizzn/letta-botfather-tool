# 🛠️ BotFather Relay Tool

A secure and efficient relay system for provisioning Telegram bots via BotFather. This tool provides a local API that enables Letta agents to interact with BotFather while maintaining security and control.

## 🚀 Features

- 🔒 Secure local API relay for BotFather interactions
- 🔄 Automatic session management and reconnection
- ⚡ Rate limiting and request validation
- 📝 Comprehensive logging and error handling
- 🔐 Optional bearer token authentication
- 🛡️ Input sanitization and validation

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
   API_BEARER_TOKEN=your_optional_bearer_token
   HOST=127.0.0.1
   PORT=57431
   LOG_LEVEL=INFO
   ```

## 🚀 Usage

1. Start the relay server:
   ```bash
   python -m botfather_relay.main
   ```

2. Send a message to BotFather:
   ```bash
   curl -X POST http://localhost:57431/send_message \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer your_token" \
     -d '{"message": "/newbot"}'
   ```

3. Example response:
   ```json
   {
     "messages": [
       "Please choose a name for your bot.",
       "Please choose a username for your bot.",
       "Great! Your bot has been created."
     ]
   }
   ```

## 🔒 Security Considerations

- The API is bound to localhost (`127.0.0.1`) by default
- Optional bearer token authentication for additional security
- Input validation and sanitization
- Rate limiting to prevent abuse
- No sensitive data logging
- Secure session management

## 📝 Logging

Logs are stored in the `logs` directory:
- Console output for immediate feedback
- Rotating file logs (10MB max, 5 backups)
- Different log levels for different components

## 🐛 Troubleshooting

1. **Authentication Issues**
   - Verify your Telegram API credentials
   - Check if your phone number is correct
   - Ensure you have a stable internet connection

2. **Connection Problems**
   - Verify the server is running
   - Check if the port is available
   - Ensure no firewall is blocking the connection

3. **Rate Limiting**
   - Default: 10 requests per minute
   - Adjust `RATE_LIMIT` and `RATE_WINDOW` in `.env` if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0) License.

You are free to:
- **Share** — copy and redistribute the material in any medium or format
- **Adapt** — remix, transform, and build upon the material for any purpose, even commercially.

Under the following terms:
- **Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.
- **ShareAlike** — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.

See the full license text at: https://creativecommons.org/licenses/by-sa/4.0/

## ⚠️ Disclaimer

This tool is part of the larger Sanctum toolset and is designed for use with Letta agents. Use responsibly and in accordance with Telegram's terms of service.
