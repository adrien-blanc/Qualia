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
async def on_ready():
    pass


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
    channel = client.get_channel(804097189081120768)

    with open('/home/Production/Qualia/server.json',"r") as f:
        data = json.load(f)
        f.close()

    category = client.get_channel(data[f"{serveur_id}"]["category"])

    for c in data[f"{serveur_id}"]["channel"]:
        for k, v in c.items():
            if (after.channel is not None) and (after.channel.id == v):
                limite = 0    
                if k == "Flex":
                    limite=5
                elif k == "DuoQ":
                    limite=2
                tempChannel = await member.guild.create_voice_channel(f"🎧{k}", user_limit=limite, category = category)
                await member.move_to(tempChannel)
                await channel.send(v)
                data[f"{serveur_id}"]["temp"] = [{member.id : tempChannel.id}]
            
                with open("/home/Production/Qualia/server.json", "w") as file:
                    json.dump(data, file, indent=4)
    
    for c in data[f"{serveur_id}"]["temp"]:
        for k, v in c.items():
            deleteChannel = client.get_channel(v)

            count = len(deleteChannel.members)
            await channel.send(count)

            if count == 0:
                await deleteChannel.delete()
                data[f"{serveur_id}"].pop("temp")
                
                with open("/home/Production/Qualia/server.json", "w") as file:
                    json.dump(data, file, indent=4)

#------------------------------------------------#
#              on raw reaction add               #
#------------------------------------------------#

@client.event
async def on_raw_reaction_add(payload):
    conn = MysqlDef.connectionBDD()
    serveur_id = payload.guild_id
    channel = client.get_channel(payload.channel_id)

    await channel.send("wait")

    messageReaction = MysqlDef.getMessageReaction(conn, serveur_id)

    for mr in messageReaction:
        msg_id = mr[0]

    if payload.message_id == msg_id:
        if payload.emoji.name == "📝":
            await channel.send("ok")






















#------------------------------------------------#
#                                                #
#           Commande d'initialisation            #
#                                                #
#------------------------------------------------#

#-------------------------------------------------------------------#
#           Initialise les Channel vocaux automatique               #
#-------------------------------------------------------------------#

@client.command()
async def initVoiceChannel(ctx):
    conn = MysqlDef.connectionBDD()
    serveur_id = ctx.guild.id

    category = None

    category = await ctx.guild.create_category("Automatic Voice Channels", overwrites=None, reason=None)
    voiceChannelGénéral = await ctx.guild.create_voice_channel("🎧Général", user_limit=0, category = category)
    voiceChannelFlex = await ctx.guild.create_voice_channel("🎧Flex", user_limit=5, category = category)
    voiceChannelDuoQ = await ctx.guild.create_voice_channel("🎧DuoQ", user_limit=2, category = category)
    MysqlDef.setServerInfo(conn, serveur_id, category.id)
    
    with open('/home/Production/Qualia/server.json',"r") as f:
        data = json.load(f)
        f.close()
    
    data[serveur_id] = {}
    data[serveur_id]['category'] = category.id
    data[serveur_id]['channel'] = [{"Général" : voiceChannelGénéral.id}, {"Flex" : voiceChannelFlex.id}, {"DuoQ" : voiceChannelDuoQ.id}]
    
    with open('/home/Production/Qualia/server.json','w') as f:
        json.dump(data, f, indent=4)
        f.close()


#-------------------------------------------------------------#
#           Initialise le message des rôles lol               #
#-------------------------------------------------------------#

@client.command()
async def initMessage(ctx):
    conn = MysqlDef.connectionBDD()
    serveur_id = ctx.guild.id

    await ctx.message.delete()

    embed=discord.Embed(title="Vous voulez rejoindre une équipe League of Legends ?")
    embed.set_author(name="Qualia E-Sport", icon_url="https://zupimages.net/up/21/13/tmqv.png") 
    msg = await ctx.channel.send(embed = embed)
    await msg.add_reaction("📝")

    MysqlDef.setMessageReaction(conn, serveur_id, msg.id)



client.run(TOKEN)