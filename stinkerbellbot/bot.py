# bot.py
import os
from discord.ext import commands
from dotenv import load_dotenv

from sillybuttons import SillyButtons

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.command(name="sillybuttons")
async def view_button(context: commands.Context):
    view = SillyButtons()
    await context.send('Press to play a sound', view=view)


bot.run(TOKEN)
