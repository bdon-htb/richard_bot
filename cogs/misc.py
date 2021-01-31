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
        if '-a' in args: # Remove the wipe message call too.
            message_check = lambda m: m.author == ctx.author
        elif '-b' in args: # Remove only bot messages of specified amount.
            message_check = lambda m: m.author.bot
        else: # Remove specified amount of user messagess NOT including the wipe message.
            message_check = lambda m: m != ctx.message and m.author == ctx.author
        await ctx.channel.purge(limit=amount, check=message_check)

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot running')

    # Commands
    @commands.command()
    async def wipe(self, ctx, amount=0, *args):
        """Usage: r!wipe [amount] [args]
        Accepted arguments:
        -a the command message is also removed
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
            print(message)
            await ctx.reply(message)

def setup(client):
    client.add_cog(Misc(client))
