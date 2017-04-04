import discord
import datetime
from discord.ext import commands
import random
import logging
from scaler.scaler import (Key, Modes)

description = '''Bot to manage The Composers Network.'''
bot = commands.Bot(command_prefix='!', description=description)

# Setting up logger
discord_logger = logging.getLogger('discord')
discord_logger.setLevel(logging.CRITICAL)
log = logging.getLogger()
log.setLevel(logging.INFO)
handler = logging.FileHandler(filename='berlioz.log', encoding='utf-8',
        mode='w')
log.addHandler(handler)

extensions = [
    'tcnexts.collab'
]

def wrapCode(text: str):
    return '```' + text + '```'

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    if not hasattr(bot, 'uptime'):
        bot.uptime = datetime.datetime.utcnow()

@bot.command()
async def scale(key: int, mode: str):
    m = ''
    if mode == 'M':
        m = Modes.Major
    elif mode == 'nm':
        m = Modes.NaturalMinor
    elif mode == 'hm':
        m = Modes.HarmonicMinor
    elif mode == 'mm':
        m = Modes.MelodicMinor

    k = Key(key, m)

    await bot.say(wrapCode(k.ppChordScale()))


if __name__ == '__main__':
    with open('token', 'r') as f:
        for extension in extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(extension,
                            type(e).__name__, e))
                
        token = f.readline().strip()
        bot.run(token)

