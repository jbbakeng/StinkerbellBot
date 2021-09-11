"""
bot.py
====================================
The core module of the StinkerbellBot
"""

import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from stinkerbellbot.sillybuttonsview import SillyButtonsView

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


class StinkerbellBot(commands.Bot):
    """The StinkerbellBot itself! Bow gracefully!"""

    def __init__(self):
        super().__init__(command_prefix='!')
        self.default_txt_channel = 'command-me'
        self.default_category = 'StinkerbellBot'

    def get_bot_text_channel(self, guild):
        return discord.utils.get(guild.channels, name=bot.default_txt_channel)

    def get_bot_channel_category(self, guild):
        return discord.utils.get(guild.categories, name=bot.default_category)


bot = StinkerbellBot()


@bot.event
async def on_ready():
    """Create a default text channel for itself where it can post messages.
    Purge the channel and set display help.
    """
    for guild in bot.guilds:
        category = bot.get_bot_channel_category(guild)
        if category is None:
            category = await guild.create_category(name=bot.default_category)
        channel = bot.get_bot_text_channel(guild)
        if channel is None:
            channel = await guild.create_text_channel(name=bot.default_txt_channel, category=category)

        deleted = await channel.purge(limit=100)


@bot.command(name="sillybuttons")
async def show_buttons(context: commands.Context):
    """Create buttons in its sillybuttons channel which will play sounds in the voice channel it has joined"""
    views = SillyButtonsView.create_sillybuttonsviews(context)
    channel = bot.get_bot_text_channel(context.guild)
    if context.channel is not channel:
        await context.reply(f"Your buttons are ready for you in the #{bot.default_txt_channel}")
    for view in views:
        await channel.send('Press to play a sound', view=view)


@bot.command(name="join")
async def bot_join(context: commands.Context):
    """Joins the same voice channel as the user"""
    voice = context.author.voice
    if voice is not None:
        try:
            await voice.channel.connect(timeout=3600)
        except discord.errors.ClientException:
            await context.reply("I'm already here NOOB!")
            return
    else:
        await context.reply(f"Hey {context.author.name}, you need to be in a voice channel "
                            f"so I know where to join!")


@bot.command(name="leave")
async def bot_leave(context: commands.Context):
    """Leaves the current voice channel"""
    voice_client = discord.utils.get(context.bot.voice_clients, guild=context.guild)
    if voice_client.is_connected():
        await voice_client.disconnect()


bot.run(TOKEN)
