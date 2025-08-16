
import os
import asyncio
from datetime import datetime, timezone
# from typing import Optional
from dotenv import load_dotenv

from motor.motor_asyncio import AsyncIOMotorClient
from rich.console import Console
from rich.prompt import Prompt

# ------------ Config ------------
load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("CHAT_DB")
COLL_USERS = "users"
COLL_MESSAGES = "messages"
ROOM = "all"  # single public room
TTL_SECONDS = 30 * 60  # 30 minutes
RECENT_LIMIT = 30  # show last N messages on join

console = Console()

# ------------ Mongo Setup ------------
client: AsyncIOMotorClient = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
users = db[COLL_USERS]
messages = db[COLL_MESSAGES]


async def ensure_indexes():
    # unique username
    await users.create_index("username", unique=True)
    # TTL on timestamp field (Mongo TTL cleaner runs ~every 60s)
    await messages.create_index("timestamp", expireAfterSeconds=TTL_SECONDS)
    # helpful secondary indexes
    await messages.create_index([("receiver", 1), ("timestamp", 1)])
    await messages.create_index([("sender", 1), ("timestamp", 1)])


# ------------ Core Ops ------------
async def register_user(username: str):
    doc = await users.find_one({"username": username})
    if not doc:
        await users.insert_one({
            "username": username,
            "created_at": datetime.now(timezone.utc),
        })


async def send_message(sender: str, text: str, receiver: str = ROOM):
    if not text.strip():
        return
    await messages.insert_one({
        "sender": sender,
        "receiver": receiver,
        "message": text,
        "timestamp": datetime.now(timezone.utc),
    })


async def show_recent_messages(username: str, limit: int = RECENT_LIMIT):
    cursor = messages.find(
        {
            "$or": [
                {"receiver": username},
                {"receiver": ROOM},
            ]
        }
    ).sort("timestamp", 1)

    # Load to list then trim last N
    all_msgs = [m async for m in cursor]
    recent = all_msgs[-limit:]

    if recent:
        console.print("[dim]— recent messages —[/dim]")
        for m in recent:
            ts = m.get("timestamp")
            ts_s = ts.astimezone().strftime("%H:%M:%S") if isinstance(ts, datetime) else "--:--:--"
            console.print(f"[cyan]{ts_s} {m['sender']}:[/cyan] {m['message']}")
        console.print("[dim]———————————————[/dim]")


# ------------ Realtime Stream ------------
async def stream_messages(username: str, stop: asyncio.Event):
    """Listen to MongoDB change stream and print new messages in realtime."""
    pipeline = [
        {"$match": {
            "operationType": {"$in": ["insert", "delete"]}
        }}
    ]

    # Note: TTL deletions produce delete events too
    try:
        async with messages.watch(pipeline=pipeline, full_document='updateLookup') as stream:
            async for change in stream:
                if stop.is_set():
                    break
                op = change.get("operationType")
                if op == "insert":
                    doc = change.get("fullDocument", {})
                    # filter visibility
                    if doc.get("receiver") in (ROOM, username):
                        ts = doc.get("timestamp")
                        ts_s = ts.astimezone().strftime("%H:%M:%S") if isinstance(ts, datetime) else "--:--:--"
                        # Move prompt up cleanly: print the message then re-render input hint
                        console.print(f"[cyan]{ts_s} {doc.get('sender')}:[/cyan] {doc.get('message')}")
                elif op == "delete":
                    # Optional: Notify about message expiry
                    # console.print("[dim]A message expired and was removed.[/dim]")
                    pass
    except Exception as e:
        console.print(f"[red]Change stream ended: {e}[/red]")


# ------------ Input Loop (async, non-blocking) ------------
async def input_loop(username: str, stop: asyncio.Event):
    console.print("[green]Type your message. Press Ctrl+C to exit.[/green]")
    while not stop.is_set():
        try:
            # run blocking input in a thread to keep event loop free
            text = await asyncio.to_thread(input, "> ")
            if text.strip() == "/quit":
                stop.set()
                break
            await send_message(username, text)
        except (EOFError, KeyboardInterrupt):
            stop.set()
            break
        except Exception as e:
            console.print(f"[red]Send failed: {e}[/red]")


# ------------ Main ------------
async def main():
    console.rule("[bold]CLI Chat (async + MongoDB)[/bold]")
    username = Prompt.ask("Choose a username").strip()

    await ensure_indexes()
    await register_user(username)
    await show_recent_messages(username)

    stop = asyncio.Event()

    # Run input and stream concurrently
    tasks = [
        asyncio.create_task(stream_messages(username, stop)),
        asyncio.create_task(input_loop(username, stop)),
    ]

    # Wait for either to stop
    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    # Signal stop and cancel remaining tasks
    stop.set()
    for t in pending:
        t.cancel()
    await asyncio.gather(*pending, return_exceptions=True)

    console.print("[red]Goodbye![/red]")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
