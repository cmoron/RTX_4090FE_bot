#!/usr/bin/env python3

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

def main():
    """
    The main function that initializes and runs the Discord bot.

    It loads the necessary environment variables, sets up the Discord intents,
    initializes the bot with a command prefix, and runs the bot using the token
    from the environment variables.
    """

    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')

    intents = discord.Intents.default()
    intents.messages = True
    intents.message_content = True

    bot = commands.Bot(command_prefix='!', intents=intents)

    @bot.event
    async def on_ready():
        """
        An asynchronous event that triggers when the bot is ready.

        Prints a message to the console indicating that the bot has successfully started.
        """
        print(f'{bot.user.name} started.')

    @bot.command()
    async def hello(ctx):
        """
        An asynchronous command that sends a greeting message.

        When a user types '!hello' in a Discord channel, the bot responds with "Hello!".
        Args:
            ctx: The context under which the command is executed.
        """
        await ctx.send("Hello!")

    bot.run(token)

if __name__ == "__main__":
    main()
