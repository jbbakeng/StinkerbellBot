# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv

from buttons import Buttons

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name="buttons")
async def view_button(context: commands.Context):
    view = Buttons()
    await context.send('Press to play a sound', view=view)


bot.run(TOKEN)
