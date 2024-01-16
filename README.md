# RTX 4090 FE Tracker Bot

## Description
This project is a Discord bot designed to track the availability of the NVIDIA RTX 4090 FE graphics card on the NVIDIA store. It notifies users when the card is back in stock, allowing them to quickly access the purchase page.

## Features
- Monitors NVIDIA store for RTX 4090 FE availability.
- Notifies users in a specific Discord channel when the card is in stock.
- Responds to user commands to check current stock status.

## Installation
To set up the bot for your use, follow these steps:

### Prerequisites
- Python 3.8 or higher
- discord.py
- A Discord Bot Token

### Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/RTX4090FE-Tracker-Bot.git
```

2. Navigate to the cloned repository:

```bash
cd RTX4090FE-Tracker-Bot
```

3. Install the required packages:

```bash
pip install -r requirements.txt
```

4. Create a .env file in the root directory and add your Discord Bot Token:

```
DISCORD_TOKEN=your_discord_bot_token
```

### Usage

To run the bot, use the following command:

```bash
python main.py
```

### Commands

* !hello: Responds with "Hello!" in the Discord chat.
