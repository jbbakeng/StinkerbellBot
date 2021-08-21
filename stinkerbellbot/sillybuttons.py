import asyncio
import discord
import json
import os

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

FFMPEG = os.getenv('FFMPEG')


class SillyButton(discord.ui.Button):

    def __init__(self, row: int, label: str, sound_file: str, context: commands.Context):
        super(SillyButton, self).__init__(label=label, row=row)
        self.context = context
        self.sound_file = sound_file

    async def callback(self, interaction: discord.Interaction):
        voice_client = discord.utils.get(self.context.bot.voice_clients, guild=self.context.guild)
        if voice_client.is_connected():
            await interaction.response.defer()
            try:
                audio_source = discord.FFmpegPCMAudio(executable=FFMPEG, source=f"./sounds/{self.sound_file}")
                voice_client.play(audio_source)
            except discord.errors.ClientException:
                await self.context.reply(f"Yo {interaction.user.name}, "
                                         f"I'm busy, wait a bit and try again.")

            while voice_client.is_playing():
                await asyncio.sleep(.1)
        else:
            await interaction.response.send_message(f"Hey {interaction.user.name}, you need to be in a voice channel "
                                                    f"so I know where to play the sound!")


class SillyButtons(discord.ui.View):

    def __init__(self, context: commands.Context):
        super(SillyButtons, self).__init__(timeout=1800)

        self.sounds_json = "./sounds/sounds.json"
        data = self.read_sounds_json()

        for sound in data['sounds']:
            self.add_item(SillyButton(0, sound['label'], sound['file_name'], context))

    def read_sounds_json(self):
        f = open(self.sounds_json, 'r')
        data = json.loads(f.read())
        print(data)
        f.close()

        return data
