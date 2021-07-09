#------------------------------------------------#
# Projet appartenant à Adrien BLANC              #
# Créé et développé par Adrien BLANC             #
# Contact : adrien.blanc74@outlook.fr            #
#------------------------------------------------#

import discord
import vars
import logging
import random
import aiocron
import asyncio
from math import *
from discord.ext import commands
from mysqlClass import MysqlDef
from pretty_help import PrettyHelp
from time import sleep
from riotwatcher import LolWatcher, ApiError # RIOT API
import datetime

#------------------------------------------------#
#                                                #
#                    RIOT API                    #
#                                                #
#------------------------------------------------#

RIOT_API_KEY = vars.RIOT_API_KEY
lol_watcher = LolWatcher(RIOT_API_KEY)
my_region = 'EUW1'


#------------------------------------------------#
#                                                #
#                      Logs                      #
#                                                #
#------------------------------------------------#

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG) # CRITICAL, ERROR, WARNING, INFO, and DEBUG and if not specified defaults to WARNING.
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

#------------------------------------------------#
#                                                #
#                     Intent                     #
#                                                #
#------------------------------------------------#

intents = discord.Intents(messages=True, guilds=True)

# If you also want reaction events enable the following:
intents.reactions = True
intents.members = True

# Somewhere else:
# client = discord.Client(intents=intents)

color = discord.Color.dark_gold()

client = commands.Bot(command_prefix='!', intents=intents, help_command=PrettyHelp(color=color, active_time=30, index_title="Help page", no_category="Main Commands", show_index=False))

#------------------------------------------------#
#                                                #
#                      Main                      #
#                                                #
#------------------------------------------------#

#------------------------------------------------#
#                Global variable                 #
#------------------------------------------------#

TOKEN = vars.TOKEN
WHITELIST_IDS = vars.WHITELIST_IDS
BLACKLIST_IDS = vars.BLACKLIST_IDS

#------------------------------------------------#
#                                                #
#                   On Ready                     #
#                                                #
#------------------------------------------------#

@client.event
async def on_ready():
    pass


client.run(TOKEN)