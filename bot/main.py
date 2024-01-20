import os
import asyncio
import discord
import nest_asyncio
from discord.ext import commands
from dotenv import load_dotenv
from bot.rtxbot import RTXBot

async def main():
    """
    The main asynchronous function to run the RTXBot.

    This function loads the necessary environment variables, initializes the Discord bot
    with the specified intents, adds the RTXBot cog to the bot, and then starts the bot.

    The bot uses a specific token for authentication and an API URL to check
    the stock availability of NVIDIA RTX 4090.
    """

    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    url = "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=fr-fr&gpu=RTX%204090&category=GPU,DESKTOP&manufacturer=NVIDIA&manufacturer_filter=NVIDIA~1,GIGABYTE~1"

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)
    await bot.add_cog(RTXBot(token, bot, url))
    await bot.run(token)

def run_main():
    """
    Program entry point.
    """
    nest_asyncio.apply()
    asyncio.run(main())
