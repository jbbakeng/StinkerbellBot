import asyncio
import discord
import json
import os

from itertools import islice
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

FFMPEG = os.getenv('FFMPEG')


class SillyButton(discord.ui.Button):

    def __init__(self, row: int, json: str, context: commands.Context):
        super(SillyButton, self).__init__(label=json['label'], row=row)
        self.context = context
        self.json = json

    async def callback(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(self.context.bot.voice_clients, guild=self.context.guild)
        if voice_client.is_connected():
            await interaction.response.defer()
            try:
                audio_source = discord.FFmpegPCMAudio(executable=FFMPEG, source=f"./sounds/{self.json['file_name']}")
                voice_client.play(audio_source)
            except discord.errors.ClientException:
                await self.context.reply(f"Yo {interaction.user.name}, "
                                         f"I'm busy, wait a bit and try again.")

            while voice_client.is_playing():
                await asyncio.sleep(.1)
        else:
            await interaction.response.send_message(f"Hey {interaction.user.name}, you need to be in a voice channel "
                                                    f"so I know where to play the sound!")


def read_sounds_json():
    sounds_json = "./sounds/sounds.json"
    f = open(file=sounds_json, mode='r', encoding='utf-8')
    data = json.loads(f.read())
    print(data)
    f.close()

    return data


def split(data, n):
    """Yield successive n-sized chunks from data."""
    it = iter(data)
    for i in range(0, len(data), n):
        yield {k: data[k] for k in islice(it, n)}


class SillyButtonsView(discord.ui.View):

    def __init__(self, context: commands.Context):
        super(SillyButtonsView, self).__init__(timeout=1800)
        self.context = context

    def add_buttons(self, buttons: str):
        row = 0
        for k, sound in enumerate(buttons):
            if k % 5 == 4:
                row += 1
            if row >= 5:
                return
            self.add_item(SillyButton(row, sound, self.context))


def create_SillyButtonsViews(context: commands.Context) -> [SillyButtonsView]:
    views = []

    sounds = read_sounds_json()['sounds']
    button_chunks = [sounds[x:x + 25] for x in range(0, len(sounds), 25)]

    for row, button_chunk in enumerate(button_chunks):
        view = SillyButtonsView(context)
        view.add_buttons(button_chunk)
        views.append(view)

    return views
