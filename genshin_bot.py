import os
from datetime import date

import requests
from discord import Intents
from discord.ext import commands
from dotenv import load_dotenv

from GenshinCharacter import GenshinCharacter

todays_date = date.today()
# Load env variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
URL = "https://genshin.jmp.blue/characters/all?lang=en"
intents = Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


async def get_char_data(url: str):
    await bot.wait_until_ready()
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception


# return a list of GenshinCharacters (with name + birthday)
async def create_genshin_character_list(genshin_characters) -> list[GenshinCharacter]:
    await bot.wait_until_ready()
    characters = []
    for character in genshin_characters:
        name = character['name']
        birthday = character['birthday'][5:]
        genshin_characters = GenshinCharacter(name, birthday)
        characters.append(genshin_characters)
    return characters


# Send happy birthday to character if birthday
async def check_birthday(character_list):
    await bot.wait_until_ready()
    day = "-".join([str(todays_date.month), str(todays_date.day)])
    channel = bot.get_channel(CHANNEL_ID)
    if channel is not None:
        for character in character_list:
            if day == character.birthday:
                await channel.send(f"Today is {character.name}'s birthday!")
                try:
                    await channel.send(f'https://genshin.jmp.blue/characters/{character.name}/card')
                except Exception as e:
                    print(e)
    else:
        print("Couldn't find channel.")


def nearest_birthday(character_list):
    # TODO: Return nearest birthday to today
    pass


async def daily_message():
    await bot.wait_until_ready()
    channel = bot.get_channel(CHANNEL_ID)
    if channel is not None:
        await channel.send("Daily Genshin update!")
    else:
        print("Couldn't find channel.")


@bot.event
async def on_ready():
    print(f'{bot.user} is now running!')


async def schedule_daily_message():
    await daily_message()
    characters = await get_char_data(URL)
    character_list = await create_genshin_character_list(characters)
    await check_birthday(character_list)


class GenshinBot(commands.Bot):
    async def setup_hook(self):
        self.bg_task = self.loop.create_task(schedule_daily_message())


if __name__ == '__main__':
    bot = GenshinBot(command_prefix='!', intents=intents)
    bot.run(TOKEN)
