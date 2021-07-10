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
import json
import os
from math import *
from discord.ext import commands
from mysqlClass import MysqlDef
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


intents = discord.Intents.default()

# If you also want reaction events enable the following:
intents.reactions = True
intents.members = True

# Somewhere else:
# client = discord.Client(intents=intents)

color = discord.Color.dark_gold()

client = commands.Bot(command_prefix='!', intents=intents)

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
#             Méthodes pré-faites                #
#                                                #
#------------------------------------------------#

#------------------------------------------------#
#                    on ready                    #
#------------------------------------------------#

@client.event
async def on_ready(): # Get serveur info into a json file.
    guilds = client.guilds

    with open("/home/Production/Qualia/serveurInfos.json", "r") as file:
        data = json.load(file)
        file.close()

    for guild in guilds:
        data[guild.id] = {}
        data[guild.id]["channel"] = []
        for channel in guild.channels:
            data[guild.id]["channel"].append(channel.id)
    
    with open("/home/Production/Qualia/serveurInfos.json", "w") as file:
        json.dump(data, file)
    channel = client.get_channel(804097189081120768)
    await channel.send("Started")


#------------------------------------------------#
#                on member join                  #
#------------------------------------------------#

@client.event
async def on_member_join(member):
    welcomeRole = discord.utils.get(member.guild.roles,name="Test") # Add spécifique rôle when member arive on serve.
    await member.add_roles(welcomeRole)


#------------------------------------------------#
#           on voice server update               #
#------------------------------------------------#

@client.event
async def on_voice_state_update(member, before, after):
    serveur_id = member.guild.id

    with open('/home/Production/Qualia/server.json',"r") as f:
        data = json.load(f)
        f.close()
    
    for item in data:
        print(item[serveur_id])

        if after.channel.id == item[serveur_id].channel[0]:
            await member.send("Alarm!")
























#------------------------------------------------#
#                                                #
#           Commande d'initialisation            #
#                                                #
#------------------------------------------------#

@client.command(brief="")
async def initVoiceChannel(ctx):
    conn = MysqlDef.connectionBDD()
    serveur_id = ctx.guild.id

    category = None

    category = await ctx.guild.create_category("Automatic Voice Channels", overwrites=None, reason=None)
    voiceChannelGénéral = await ctx.guild.create_voice_channel("🎧Général", category = category)
    voiceChannelFlex = await ctx.guild.create_voice_channel("🎧Flex", category = category)
    voiceChannelDuoQ = await ctx.guild.create_voice_channel("🎧DuoQ", category = category)
    MysqlDef.setServerInfo(conn, serveur_id, category.id)
    
    with open('/home/Production/Qualia/server.json',"r") as f:
        data = json.load(f)
        f.close()
    
    data[serveur_id] = {}
    data[serveur_id]['category'] = category.id
    data[serveur_id]['channel'] = [{"General" : voiceChannelGénéral.id}, {"Flex" : voiceChannelFlex.id}, {"DuoQ" : voiceChannelDuoQ.id}]
    
    with open('/home/Production/Qualia/server.json','w') as f:
        json.dump(data, f, indent=4)
        f.close()






client.run(TOKEN)