import argparse
from telethon_client import BotFatherSession
import asyncio
import sys
import json
import logging

# Configure logging
logger = logging.getLogger(__name__)

def setup_logging(verbose: bool):
    """Configure logging based on verbosity."""
    level = logging.INFO if verbose else logging.WARNING
    logging.basicConfig(level=level)

def main():
    parser = argparse.ArgumentParser(
        description="""BotFather CLI tool - A command-line interface for interacting with Telegram's BotFather

Output:
  By default, all output is in JSON format and logging is disabled.
  Use --verbose to enable detailed logging output.""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Global arguments
    parser.add_argument('--verbose', '-v', action='store_true',
                      help='Enable verbose logging output (default: disabled)')
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands", metavar="COMMAND")

    # Send message command
    send_parser = subparsers.add_parser("send-message", 
                                      help="Send a message to BotFather",
                                      description="""Send a message to BotFather.

Required Arguments:
  --msg TEXT     The message to send to BotFather

Optional Arguments:
  --verbose, -v  Enable verbose logging output (default: disabled)

Output:
  JSON format containing:
    - id: Message ID
    - text: Message text""",
                                      formatter_class=argparse.RawDescriptionHelpFormatter)
    send_parser.add_argument("--msg", required=True,
                           help="Message to send to BotFather")

    # Get replies command
    get_parser = subparsers.add_parser("get-replies",
                                     help="Get replies from BotFather",
                                     description="""Get replies from BotFather.

Optional Arguments:
  --limit N      Number of replies to fetch (default: 1)
  --verbose, -v  Enable verbose logging output (default: disabled)

Output:
  JSON format containing an array of messages, each with:
    - id: Message ID
    - text: Message text
    - buttons: Array of button rows (if present)""",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    get_parser.add_argument("--limit", type=int, default=1,
                          help="Number of replies to fetch (default: 1)")

    # Click button command
    click_parser = subparsers.add_parser("click-button",
                                       help="Press an inline button in a BotFather reply",
                                       description="""Press an inline button in a BotFather reply.

Optional Arguments:
  --msg-id MSG_ID     The ID of the message containing the button (default: last message)
  --button-text TEXT  The visible text of the button to press
  --row ROW           The row index of the button (0-based, used with --col)
  --col COL           The column index of the button (0-based, used with --row)
  --verbose, -v       Enable verbose logging output

Button Selection (choose one):
  --button-text TEXT  The visible text of the button to press
  --row ROW           The row index of the button (0-based, used with --col)
  --col COL           The column index of the button (0-based, used with --row)

Output:
  JSON format containing:
    - id: Message ID
    - button: Button text or (row, col)
    - result: Result of the button press (text or message)
    - status: "success" or "error" """,
                                       formatter_class=argparse.RawDescriptionHelpFormatter)
    click_parser.add_argument("--msg-id", type=int,
                            help="The ID of the message containing the button (default: last message)")
    click_group = click_parser.add_mutually_exclusive_group(required=True)
    click_group.add_argument("--button-text",
                           help="The visible text of the button to press")
    click_group.add_argument("--row", type=int,
                           help="The row index of the button (0-based, used with --col)")
    click_parser.add_argument("--col", type=int,
                            help="The column index of the button (0-based, used with --row)")

    args = parser.parse_args()
    
    # Setup logging based on verbosity
    setup_logging(args.verbose)
    
    if not args.command:
        parser.print_help()
        sys.exit(1)

    session = BotFatherSession()

    async def run():
        try:
            await session.start()
            if args.command == "send-message":
                result = await session.send_message("BotFather", args.msg)
                print(json.dumps(result, indent=2))
            elif args.command == "get-replies":
                replies = await session.get_replies("BotFather", args.limit)
                print(json.dumps(replies, indent=2))
            elif args.command == "click-button":
                if args.button_text:
                    result = await session.click_button(args.msg_id, button_text=args.button_text)
                else:
                    if args.row is None or args.col is None:
                        parser.error("Both --row and --col must be specified when using position-based selection")
                    result = await session.click_button(args.msg_id, row=args.row, col=args.col)
                print(json.dumps(result, indent=2))
            else:
                parser.print_help()
        except Exception as e:
            logger.error(f"Error: {e}")
            sys.exit(1)
        finally:
            await session.stop()

    asyncio.run(run())

if __name__ == '__main__':
    main() 