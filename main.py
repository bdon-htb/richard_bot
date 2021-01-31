import discord

try:
    from bot_token import TOKEN
except ImportError as e:
    raise ImportError('Error while trying to get the token. Did you make sure to include bot_token.py?')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)
