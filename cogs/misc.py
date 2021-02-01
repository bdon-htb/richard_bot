import discord
from discord.ext import commands

import random
# Custom imports
import cfg

class Misc(commands.Cog):
    """A class containing miscellaneous command implementations.
    """

    def __init__(self, client):
        self.client = client

    async def _wipe_helper(self, ctx, amount, args=[]):
        """Handles the removal of messages for r!wipe.
        """
        if '-a' in args: # Remove the wipe message call too.
            message_check = lambda m: m.author == ctx.author
        elif '-b' in args: # Remove only bot messages of specified amount.
            message_check = lambda m: m.author.bot
        else: # Remove specified amount of user messagess NOT including the wipe message.
            message_check = lambda m: m != ctx.message and m.author == ctx.author
        await ctx.channel.purge(limit=amount, check=message_check, bulk=True)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot running')

    # Commands
    @commands.command()
    async def help(self, ctx, c=''):
        """Dynamically construct a help message containing commands and
        their usage. If a valid command is specified then the bot will
        send a help message of the specific command the method's docstring.

        Usage: {PREFIX}help [c: str]
        [c] is the name of any bot command.
        """
        # Checker function checks that it's not a private method or a listener
        commands = self.get_commands()
        com_names = [com.name for com in commands]

        if c in com_names:
            method = commands[com_names.index(c)].callback
            docstring = method.__doc__.replace('{PREFIX}', cfg.PREFIX)
            message = f'```===Documentation for {c}===\n'
            for line in docstring.split('\n'):
                message += line.lstrip() + '\n'
            message += '```'
            await ctx.send(message)
        else:
            message = '```===List of Commands===\n'
            for name in com_names:
                message += cfg.PREFIX + name + '\n'
            message += '```'
            await ctx.send(message)

    @commands.command()
    async def wipe(self, ctx, amount=0, *args):
        """Delete message(s) from the server.

        Usage: {PREFIX}wipe [amount: int] [args]
        [amount] the number of messages to remove (command itself not included)

        Accepted arguments:
        -a the command message is also removed.
        -b removes only messages by bots.
        -s stops the bot from sending the success message.
        """
        channel = ctx.channel.name
        valid_channels = cfg.SETTINGS['wipe_channel']

        if '-a' in args:
            amount += 1

        if amount > 0 and (valid_channels == [] or channel in valid_channels):
            message = random.choice(cfg.WORDS['success']) + ' ' + ctx.author.name
            message += f'. Just purged {amount} messages'
            await self._wipe_helper(ctx, amount, args)
        else:
            message = random.choice(cfg.WORDS['failed']) + ' ' + ctx.author.name
            if amount <= 0:
                message += f'. I can\'t delete {amount} messages.'
            else:
                message += '. I\'ve been told not to delete messages in this channel.'

        if '-s' not in args:
            if '-a' in args:
                await ctx.send(message)
            else:
                await ctx.reply(message)

def setup(client):
    client.add_cog(Misc(client))
