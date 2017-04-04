from bs4 import BeautifulSoup
from urllib.request import urlopen
from discord.ext import commands

import json

test_url='https://soundcloud.com/mvy/sets/private-pl/s-qhbqj'
sc_prefix='https://soundcloud.com'


class Collab:

    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def collab(self, ctx):
        if ctx.invoked_subcommand is None:
            await self.bot.say('Incorrect collab subcommand.')
            await self.bot.say('Currently available commands are :')
            await self.bot.say('`!collab set <url>`')
            await self.bot.say('`!collab next`')

    @collab.command(pass_context=True)
    async def set(self, ctx, url):
        if 'soundcloud.com' not in url:
            await self.bot.say('Not a soundcloud address.')
            return

        html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')
        for section in soup.find_all('section'):
            links = []

            if 'tracklist' in section['class']:
                articles = section.find_all('article')
                for article in articles:
                    links.append(article.h2.a['href'])

        with open('tmp/data' + ctx.message.channel.id + '.txt', 'w') as outfile:
            data = {
                'urls': links,
                'current': 0
            }

            json.dump(data, outfile)

        outfile.close()

        await self.bot.say('Collaboration games playlist initialised with ' +
            len[links] + ' songs.')

    @collab.command(pass_context=True)
    async def next(self, ctx):
        with open('tmp/data' + ctx.message.channel.id + '.txt', 'r') as infile:
            data = json.load(infile)

        infile.close()

        if data == None:
            await self.bot.say('Playlist is empty, please initialise with ' +
                '`!collab set <url>` first.')
            return

        number = data['current']
        urls = data['urls']

        if number < 0:
            await self.bot.say('Error in reading the playlist, please contact a ' 
                ' TCN IT scientist.')
            return 

        if number >= len(urls):
            await self.bot.say('The playlist has been exhausted. Please reset it '
                'if you need more songs.')
            return 

        await self.bot.say(sc_prefix + urls[number])
        number += 1

        with open('tmp/data' + ctx.message.channel.id + '.txt', 'w') as outfile:
            data = {
                'urls': urls,
                'current': number
            }
            json.dump(data, outfile)

        outfile.close()

def setup(bot):
    bot.add_cog(Collab(bot))
