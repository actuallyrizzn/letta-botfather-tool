# Part Two: Tool Function for Testing & Integration Checklist

## 🎯 Core Requirements

### Python Function
- [x] Implement `provision_botfather_message(message: str) -> List[str]`
- [x] Use only Python standard library and `requests` (no extra dependencies)
- [x] Function sends POST request to `http://localhost:57431/send_message`
- [x] Function returns a list of BotFather replies
- [x] Add clear docstrings and comments
- [x] Handle connection errors, timeouts, and invalid responses

### CLI Interface
- [x] Implement CLI entry point using `argparse`
- [x] Allow usage: `python botfather.py "/newbot"`
- [x] Print BotFather responses in a human-readable way
- [x] Add help and usage messages

### Documentation
- [ ] Add usage examples for both function and CLI
- [ ] Document expected responses and error formats
- [ ] Provide integration instructions for Monday's framework

### Testing
- [x] Write minimal test script for typical use and error cases
- [x] Test function with valid and invalid messages
- [x] Test CLI with various arguments
- [x] Ensure error handling is robust

## ⚠️ Negative Prompts (What NOT to Do)

### Security
- ❌ Never hardcode sensitive data or tokens
- ❌ Don't log sensitive information
- ❌ Don't allow remote relay URLs (localhost only)

### Code Quality
- ❌ Don't use non-standard libraries (only stdlib + requests)
- ❌ Don't skip error handling
- ❌ Don't skip docstrings or comments
- ❌ Don't use magic numbers or strings
- ❌ Don't use global variables

### Usability
- ❌ Don't make CLI output hard to read
- ❌ Don't skip argument validation
- ❌ Don't ignore exit codes on error

### Testing
- ❌ Don't skip tests for error scenarios
- ❌ Don't ignore edge cases
- ❌ Don't skip manual CLI testing

## 📝 Implementation Notes

### Required Dependencies
- Python 3.7+
- requests

### File Structure
```
botfather.py
```

### Example Usage
```bash
python botfather.py "/newbot"
```

### Expected Response Format
```json
{
  "messages": [
    "BotFather reply 1",
    "BotFather reply 2",
    "BotFather reply 3"
  ]
}
```

## 🔄 Development Workflow

1. Implement core function
2. Add CLI interface
3. Write docstrings and comments
4. Test function and CLI
5. Document usage and integration
6. Write and run tests

## 🚀 Deployment Checklist

- [ ] All requirements met
- [ ] Function and CLI tested
- [ ] Documentation complete
- [ ] Example usage verified
- [ ] Error handling validated
- [ ] Ready for integration 