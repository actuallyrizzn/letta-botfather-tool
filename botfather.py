# Set RELAY_HOST and RELAY_PORT directly here.
# For Docker (containerized Letta, relay on host or another container):
# RELAY_HOST = 'host.docker.internal'  # or the container name if using Docker Compose networking
# RELAY_PORT = '57431'
#
# For non-Docker (all running on the same host):
RELAY_HOST = 'localhost'
RELAY_PORT = '57431'

import argparse
import requests
import json
from typing import List

def botfather(message: str) -> List[str]:
    """
    Sends a message to BotFather via the relay API and returns the list of replies.

    Args:
        message (str): The message to send to BotFather.

    Returns:
        List[str]: A list of BotFather replies.

    Raises:
        requests.RequestException: If there is an error connecting to the relay.
        ValueError: If the response is invalid or an error is returned.
    """
    url = f"http://{RELAY_HOST}:{RELAY_PORT}/send_message"
    payload = {"message": message}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        if "messages" in data:
            return data["messages"]
        else:
            raise ValueError("Invalid response format: 'messages' key not found")
    except requests.RequestException as e:
        raise requests.RequestException(f"Error communicating with relay: {e}")
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON response from relay")

def main():
    parser = argparse.ArgumentParser(description="Send a message to BotFather via the relay API.")
    parser.add_argument("message", type=str, help="The message to send to BotFather")
    args = parser.parse_args()

    try:
        replies = botfather(args.message)
        print("BotFather replies:")
        for i, reply in enumerate(replies, 1):
            print(f"{i}. {reply}")
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main() 