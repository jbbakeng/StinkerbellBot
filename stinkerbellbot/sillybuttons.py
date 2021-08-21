import asyncio
import discord
import json
import os

from dotenv import load_dotenv

load_dotenv()

FFMPEG = os.getenv('FFMPEG')


class SillyButton(discord.ui.Button):

    def __init__(self, row: int, label: str, sound_file: str):
        super(SillyButton, self).__init__(label=label, row=row)
        self.sound_file = sound_file

    async def callback(self, interaction: discord.Interaction):
        voice = interaction.user.voice
        if voice is not None:
            try:
                vc = await voice.channel.connect()
            except discord.errors.ClientException:
                await interaction.response.send_message(f"Yo {interaction.user.name}, "
                                                        f"I'm busy, wait a bit and try again.")
                return

            await interaction.response.defer()
            audio_source = discord.FFmpegPCMAudio(executable=FFMPEG, source=f"./sounds/{self.sound_file}")
            vc.play(audio_source)

            while vc.is_playing():
                await asyncio.sleep(.1)
            await vc.disconnect()
        else:
            await interaction.response.send_message(f"Hey {interaction.user.name}, you need to be in a voice channel "
                                                    f"so I know where to play the sound!")


class SillyButtons(discord.ui.View):

    def __init__(self):
        super(SillyButtons, self).__init__(timeout=1800)

        self.sounds_json = "./sounds/sounds.json"
        data = self.read_sounds_json()

        for sound in data['sounds']:
            self.add_item(SillyButton(0, sound['label'], sound['file_name']))

    def read_sounds_json(self):
        f = open(self.sounds_json, 'r')
        data = json.loads(f.read())
        print(data)
        f.close()

        return data
