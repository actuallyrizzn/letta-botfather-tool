import argparse
from telethon_client import BotFatherSession
import asyncio
import sys

# CLI entry point for BotFather actions

def main():
    parser = argparse.ArgumentParser(description="BotFather CLI tool")
    subparsers = parser.add_subparsers(dest="command")

    send_parser = subparsers.add_parser("send-message", help="Send a message to BotFather")
    send_parser.add_argument("--msg", required=True, help="Message to send to BotFather")

    get_parser = subparsers.add_parser("get-replies", help="Get replies from BotFather")
    get_parser.add_argument("--limit", type=int, default=3, help="Number of replies to fetch from BotFather")

    args = parser.parse_args()
    session = BotFatherSession()

    async def run():
        try:
            await session.start()
            if args.command == "send-message":
                result = await session.send_message("BotFather", args.msg)
                print(f"Message sent. ID: {result['id']}")
                print(f"Text: {result['text']}")
            elif args.command == "get-replies":
                replies = await session.get_replies("BotFather", args.limit)
                for i, reply in enumerate(replies, 1):
                    print(f"Reply {i}:")
                    print(f"  ID: {reply['id']}")
                    print(f"  Text: {reply['text']}")
                    if 'buttons' in reply and reply['buttons']:
                        print(f"  Buttons: {reply['buttons']}")
            else:
                parser.print_help()
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            await session.stop()

    asyncio.run(run())

if __name__ == '__main__':
    main() 