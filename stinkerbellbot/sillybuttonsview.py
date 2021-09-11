import discord
import json

from itertools import islice
from discord.ext import commands

from stinkerbellbot.sillybutton import SillyButton


def read_sounds_json():
    """read_sounds_json"""
    sounds_json = "./sounds/sounds.json"
    f = open(file=sounds_json, mode='r', encoding='utf-8')
    data = json.loads(f.read())
    f.close()

    return data


def split(data, n):
    """Yield successive n-sized chunks from data."""
    it = iter(data)
    for i in range(0, len(data), n):
        yield {k: data[k] for k in islice(it, n)}


class SillyButtonsView(discord.ui.View):
    """A view containing up to 25 silly buttons"""

    def __init__(self, context: commands.Context):
        """init"""
        super(SillyButtonsView, self).__init__(timeout=1800)
        self.context = context

    def add_buttons(self, buttons: str):
        """add_buttons"""
        row = -1
        for k, sound in enumerate(buttons):
            if k % 5 == 0:
                row += 1
            if row >= 5:
                return
            self.add_item(SillyButton(row, sound, self.context))

    @staticmethod
    def create_sillybuttonsviews(context: commands.Context) -> []:
        """create_sillybuttonsviews"""
        views = []

        sounds = read_sounds_json()['sounds']
        button_chunks = [sounds[x:x + 25] for x in range(0, len(sounds), 25)]

        for row, button_chunk in enumerate(button_chunks):
            view = SillyButtonsView(context)
            view.add_buttons(button_chunk)
            views.append(view)

        return views
