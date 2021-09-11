import asyncio

import discord
from discord.ext import commands

import os
from dotenv import load_dotenv


load_dotenv()

FFMPEG = os.getenv('FFMPEG')



class SillyButton(discord.ui.Button):
    """A button able to play a connected sound"""

    def __init__(self, row: int, json: str, context: commands.Context):
        """init"""
        super(SillyButton, self).__init__(label=json['label'], row=row)
        self.context = context
        self.json = json

    async def callback(self, interaction: discord.Interaction):
        """Callback"""
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