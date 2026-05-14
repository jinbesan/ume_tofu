# ume_tofu

A Discord bot that manages a sales sheet and responds to messages using LLM.

## Features

- **Sales tracking** - Add/undo items to a Google Sheet via commands
- **LLM responder** - Randomly responds to messages with personality-driven responses
- Configurable response chances for different message types

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure `.env`:
   ```bash
   DISCORD_TOKEN=your_discord_bot_token
   GROQ_API_KEY=your_groq_api_key
   GROQ_MODEL=llama-3.1-8b-instant
   RESPONSE_CHANCE=0.03
   RESPONSE_CHANCE_SHRIMP=0.67
   RESPONSE_CHANCE_HELP=0.25
   RESPONSE_CHANCE_MENTIONED=1
   ```

3. Set up Google Sheets credentials:
   - Place `ume-tofu-tracker-creds.json` in the project root
   - Update the spreadsheet ID in `tracker.py` if needed

4. Run:
   ```bash
   python main.py
   ```

## Commands

| Command | Description |
|---------|-------------|
| `ume add <items>` | Add items to sales sheet (comma-separated) |
| `ume undo` | Undo last transaction |
| `ume inspire` | Get inspirational quote |
| `ume hello` | Get a greeting |
| `ume help` | Show help message |
| `ume responding <true/false>` | Toggle responding |

## LLM Responder

The bot randomly responds to messages based on content:
- Messages containing "help" - higher response chance
- Messages containing "shrimp" or "pink" - higher response chance
- When bot is mentioned - highest response chance
- All other messages - base response chance

Personality and tone are defined in `utils/llm.py`.