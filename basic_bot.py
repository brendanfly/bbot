import discord
from discord.ext import commands
import random
import urllib.request
from bs4 import BeautifulSoup
import json

description = '''An example bot to showcase the discord.ext.commands extension
module.

There are a number of utility commands being showcased here.'''
bot = commands.Bot(command_prefix='mb!', description=description)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# bot command to display top 10 MDL players
@bot.command()
async def mdl():
    """displays the top 10 on Deadman's MDL"""
    mdl_url = "http://md-ladder.cloudapp.net/api/v1.0/players/?topk=10"

    content = urllib.request.urlopen(mdl_url).read()

    data = json.loads(content)
    await bot.say("Deadman's Multi-Day Ladder Top 10")
    await bot.say("=================================")
    current_player = 1
    for index, player in enumerate(data['players']):
        # once we have the players, start printing out each of the top 10
        await bot.say(str(current_player) + ") " + player['player_name'] + " Rating:" + str(player['displayed_rating']))
        current_player += 1

# bot command to display top 10 ladder players
@bot.command()
async def ladders():
    """displays the top 10 on all WL ladders"""
    ladder_pageurls = ['https://www.warzone.com/LadderSeason?ID=0', 'http://www.warzone.com/LadderSeason?ID=1',
                       'https://www.warzone.com/LadderSeason?ID=4']
    for ladder_pageurl in ladder_pageurls:
        ladder_page = urllib.request.urlopen(ladder_pageurl)
        soup = BeautifulSoup(ladder_page, 'html.parser')
        tables = soup.find_all('table')

        header_str = soup.title.string.split("-")
        for table in tables:
            data = "__" + header_str[0].strip() + "__"
            rows = table.find_all('tr')
            for row in rows:
                columns = row.find_all('td')
                for column in columns:
                    if column.contents[0].strip() and "Rank" in column.contents[0].strip():
                        found_table = True
                        break
                    elif len(columns) == 3:
                        rating_column = columns[2]
                        team_column = columns[1]
                        data = columns[0].contents[0].strip()
                        data += ") "
                        current_link = 0
                        for link in team_column.find_all('a'):
                            if "LadderTeam" in link.get('href'):
                                if (link.contents[0].strip()) != "":
                                    data += link.contents[0].strip() + " "
                                current_link += 1
                                if (current_link > 1) and (current_link < len(columns)):
                                    data += "/ "

                        data += " Rating: " + rating_column.contents[0]
                await bot.say(data)
            if found_table:
                found_table = False
                await bot.say("====================================================")
                break

@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

@cool.command(name='bot')
async def _bot():
    """Is the bot cool?"""
    await bot.say('Yes, the bot is cool.')

bot.run('NDE5MjU2OTU2ODk3NzIyMzg5.DXycMQ.OMAH2tx9kQBISJtPfZ7rqH6TPt8')
