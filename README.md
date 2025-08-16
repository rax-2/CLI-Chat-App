# 🗨️ Async CLI Chat App

[![Python](https://img.shields.io/badge/python-3.9%2B-blue?logo=python)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-green?logo=mongodb)](https://www.mongodb.com/)
[![Asyncio](https://img.shields.io/badge/asyncio-Concurrency-orange?logo=python)](https://docs.python.org/3/library/asyncio.html)
[![Motor](https://img.shields.io/badge/Motor-Async%20MongoDB-blue)](https://motor.readthedocs.io/)
[![Rich](https://img.shields.io/badge/Rich-CLI%20UI-purple)](https://github.com/Textualize/rich)
[![dotenv](https://img.shields.io/badge/dotenv-Env%20Vars-lightgrey)](https://pypi.org/project/python-dotenv/)
[![Built with AI](https://img.shields.io/badge/Built%20with-AI-red?logo=openai)](https://openai.com/)

A **realtime command-line chat application** built with **Python (asyncio)** and **MongoDB**. Messages appear live across all connected clients using **MongoDB Change Streams**, and old messages auto-expire after **30 minutes** using a **TTL index**.

---

## 🚀 Features

* 🔄 **Realtime chat** powered by MongoDB Change Streams.
* 🧑‍🤝‍🧑 Public chatroom (`all`) with support for DMs (extendable).
* 🕒 Auto-delete messages after **30 minutes** (TTL index).
* ⏱ Shows recent chat history when joining.
* ✨ Beautiful CLI output with `rich`.
* ⚡ Async + non-blocking input (smooth typing + live updates).
* 🤖 **Assisted & scaffolded with AI** during development.

---

## 🛠️ Tech Stack

* **Python** (3.9+)
* **asyncio** – concurrency
* **Motor** – async MongoDB driver
* **MongoDB** – database + change streams + TTL
* **Rich** – styled CLI output
* **python-dotenv** – load `.env` config
* **AI Assistance** – design & development scaffolding

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

* Choose a username when prompted.
* Type messages to chat in realtime.
* Use `/quit` or `Ctrl+C` to exit.

---

## ⚙️ Configuration

* `TTL_SECONDS` → how long messages live (default: 1800 = 30min)
* `RECENT_LIMIT` → how many past messages to show when joining

---

