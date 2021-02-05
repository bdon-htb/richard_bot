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

    async def _clear(self, ctx, n, is_valid):
        """Removes n number of messages. Counter only goes up when message
        passes the is_valid function.

        Precondition: n > 0
        """
        async for message in ctx.channel.history():
            if n <= 0:
                break
            elif is_valid(message):
                await message.delete()
                n -= 1

    async def _bulk_clear(self, ctx, n, is_valid):
        """Does a bulk clear of messages using purge.
        Favours speed over accuracy.
        """
        await ctx.channel.purge(limit=n, check=is_valid, bulk=True)


    async def _wipe_helper(self, ctx, amount, args=[]):
        """Handles the removal of messages for r!wipe.
        """
        if '-a' in args: # Remove the wipe message call too.
            message_check = lambda m: m.author == ctx.author
        elif '-b' in args: # Remove only bot messages of specified amount.
            message_check = lambda m: m.author.bot
        else: # Remove specified amount of user messagess NOT including the wipe message.
            message_check = lambda m: m != ctx.message and m.author == ctx.author

        if amount > 25:
            await self._bulk_clear(ctx, amount, message_check)
        else:
            await self._clear(ctx, amount, message_check)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot running')

    # Commands
    @commands.command()
    async def help(self, ctx, c=''):
        """Dynamically construct a help message containing commands and
        their usage. If a valid command is specified then the bot will
        send a help message of the specific command using the method's
        docstring.

        Usage: {PREFIX}help [c: str]
        [c] is the name of any bot command.
        """
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

            message += f'\nIf you need help with using a particular command\nadd the name of it to {cfg.PREFIX}help.\ni.e. {cfg.PREFIX}help wipe```'
            await ctx.send(message)

    @commands.command()
    async def wipe(self, ctx, amount=0, *args):
        """Delete message(s) from the server.

        Usage: {PREFIX}wipe [amount: int] [args]
        [amount] is the number of messages to remove.
        The command message is not included by default.

        Note:
        If [amount] is greater than 25 the bot will fallback to a bulk
        delete implementations which won't be as accurate.

        Accepted arguments:
        -a include the command message in deletion.
        -b wipe only the last [amount] messages by bots.
        -s stops the bot from sending the success message.
        """
        channel = ctx.channel.name
        valid_channels = cfg.SETTINGS['wipe_channel']

        if '-a' in args:
            amount += 1

        if amount > 0 and (valid_channels == [] or channel in valid_channels):
            message = random.choice(cfg.WORDS['success']) + ' ' + ctx.author.name
            message += f'. Purged {amount} messages'
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
