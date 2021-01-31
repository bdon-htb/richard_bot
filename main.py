import discord
from discord.ext import commands

import os

# Setup logging.
import logging
logging.basicConfig(level=logging.INFO)

# Custom modules
import cfg

# TODO: One the bot is complete. remove bot_token.py from .gitignore and
# instead just have TOKEN be an empty string for the end user to change.
try:
    from bot_token import TOKEN
except ImportError:
    raise ImportError('Error while trying to get the token. Did you make sure to include bot_token.py?')

client = commands.Bot(command_prefix = cfg.PREFIX)

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

# Load all cogs from /cogs/
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(TOKEN)
