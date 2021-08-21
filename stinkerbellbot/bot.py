# bot.py
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

from sillybuttons import SillyButtons

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name="sillybuttons")
async def show_buttons(context: commands.Context):
    view = SillyButtons()
    await context.send('Press to play a sound', view=view)


@bot.command(name="join")
async def bot_join(context: commands.Context):
    voice = context.author.voice
    if voice is not None:
        try:
            voice_channel = await voice.channel.connect(timeout=3600)
        except discord.errors.ClientException:
            await context.reply("I'm already here NOOB!")
            return
    else:
        await context.reply(f"Hey {context.author.name}, you need to be in a voice channel "
                            f"so I know where to join!")


@bot.command(name="leave")
async def bot_leave(context: commands.Context):
    voice_client = discord.utils.get(context.bot.voice_clients, guild=context.guild)
    if voice_client.is_connected():
        await voice_client.disconnect()


bot.run(TOKEN)
