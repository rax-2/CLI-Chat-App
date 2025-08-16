# 🗨️ Async CLI Chat App

&#x20;   &#x20;

A **realtime command-line chat application** built with **Python (asyncio)** and **MongoDB**. Messages appear live across all connected clients using **MongoDB Change Streams**, and old messages auto-expire after **30 minutes** using a **TTL index**.

---

## 🚀 Features

- 🔄 **Realtime chat** powered by MongoDB Change Streams.
- 🧑‍🤝‍🧑 Public chatroom (`all`) with support for DMs (extendable).
- 🕒 Auto-delete messages after **30 minutes** (TTL index).
- ⏱ Shows recent chat history when joining.
- ✨ Beautiful CLI output with `rich`.
- ⚡ Async + non-blocking input (smooth typing + live updates).

---

## 🛠️ Tech Stack

- **Python** (3.9+)
- **asyncio** – concurrency
- **Motor** – async MongoDB driver
- **MongoDB** – database + change streams + TTL
- **Rich** – styled CLI output
- **python-dotenv** – load `.env` config

---

## 📦 Installation

1. Clone this repo:

```bash
git clone https://github.com/yourusername/cli-chat-app.git
cd cli-chat-app
```

2. Install dependencies:

```bash
pip install motor rich python-dotenv
```

3. Set up environment variables in a `.env` file:

```env
MONGODB_URI=mongodb://localhost:27017
CHAT_DB=chat_app
```

4. Start MongoDB (local or Atlas).

---

## ▶️ Usage

Run the app in multiple terminals (one per user):

```bash
python chat_async.py
```

- Choose a username when prompted.
- Type messages to chat in realtime.
- Use `/quit` or `Ctrl+C` to exit.

---

## ⚙️ Configuration

- `TTL_SECONDS` → how long messages live (default: 1800 = 30min)
- `RECENT_LIMIT` → how many past messages to show when joining

---

## 📌 Roadmap

-

---

## 📝 License

MIT License. Free to use, modify, and share.

