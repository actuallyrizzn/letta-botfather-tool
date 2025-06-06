# Part 3: Dockerizing the BotFather Relay API

This guide describes how to containerize the BotFather relay API using Docker, ensuring process and session isolation from other Telethon-based services on the same machine.

---

## Why Dockerize?
- **Isolation:** Prevents session/database locking issues by running the relay in its own environment.
- **Portability:** Easy to deploy, update, and move between hosts.
- **Maintainability:** Keeps dependencies and runtime separate from other services.

---

## Step 1: Create a Dockerfile

In the project root (where `botfather_relay/` and `requirements.txt` live), create a file named `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HOST=0.0.0.0
ENV PORT=57431

CMD ["python", "-m", "botfather_relay.main"]
```

---

## Step 2: Build the Docker Image

From the project root, run:

```bash
docker build -t botfather-relay:latest .
```

---

## Step 3: Run the Container

Run the relay API in a detached container, exposing the correct port and passing required environment variables:

```bash
docker run -d \
  --name botfather-relay \
  -p 57431:57431 \
  -e TELEGRAM_API_ID=your_api_id \
  -e TELEGRAM_API_HASH=your_api_hash \
  -e TELEGRAM_PHONE=your_phone_number \
  -e API_BEARER_TOKEN=your_optional_bearer_token \
  -e HOST=0.0.0.0 \
  -e PORT=57431 \
  botfather-relay:latest
```

- **Do not mount or share the session file with any other container or the host.**
- The relay will now be accessible at `http://host.docker.internal:57431` from other containers (e.g., Letta) on the same machine.

---

## Step 4: Update Letta Tool Configuration

In your Letta tool (inside its own container), set the following environment variables:

```
RELAY_HOST=host.docker.internal
RELAY_PORT=57431
```

This allows the Letta tool to reach the relay API running in its own container.

---

## Notes
- If you use Docker Compose, you can define both services and use Docker networking for service discovery.
- Always use a unique session file per container/account.
- For production, consider using secrets management for API keys and tokens.

---

**This approach ensures the BotFather relay API is fully isolated, avoids session/database locking, and is easy to deploy and maintain.** 