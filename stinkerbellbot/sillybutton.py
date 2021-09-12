import asyncio

from discord import ButtonStyle, PartialEmoji, FFmpegPCMAudio, errors, utils, ui, Interaction
from discord.ext import commands

import os
from dotenv import load_dotenv

load_dotenv()

FFMPEG = os.getenv('FFMPEG')


class SillyButton(ui.Button):
    """A button able to play a connected sound"""

    def __init__(self, row: int, json: str, context: commands.Context):
        """init"""
        super(SillyButton, self).__init__(label=json['label'], row=row)
        self.context = context
        self.json = json

    async def update_button_style(self, interaction, style: ButtonStyle, emoji: PartialEmoji = None):
        """Set a button style and update the view"""

        self.style = style
        self.emoji = emoji
        await interaction.message.edit(view=self.view)

    async def callback(self, interaction: Interaction):
        """Callback handling what actions to perform when a button is clicked"""

        voice_client = utils.get(self.context.bot.voice_clients, guild=self.context.guild)

        # If the bot is in a voice channel
        if voice_client.is_connected():
            await interaction.response.defer()

            # Try to play the sound,
            # if a sound is already playing or it cannot be played the bot will notify the user
            try:
                audio_source = FFmpegPCMAudio(executable=FFMPEG, source=f"./sounds/{self.json['file_name']}")
                voice_client.play(audio_source)
            except errors.ClientException:
                await self.context.reply(f"Yo {interaction.user.name}, "
                                         f"I'm busy, wait a bit and try again.")
                return

            # Change the style of the button that is playing a sound
            while voice_client.is_playing():
                if self.style != ButtonStyle.green:
                    await self.update_button_style(interaction, ButtonStyle.green, PartialEmoji(name='🔊'))
                await asyncio.sleep(.1)
            await self.update_button_style(interaction, ButtonStyle.grey)

        else:
            # If the bot is NOT in a voice channel
            await interaction.response.send_message(f"Hey {interaction.user.name}, you need to be in a voice channel "
                                                    f"so I know where to play the sound!")
