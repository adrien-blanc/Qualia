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




# If you also want reaction events enable the following:
intents = discord.Intents.all()
intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)

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
    pass
    #welcomeRole = discord.utils.get(member.guild.roles,name="Test") # Add spécifique rôle when member arive on serve.
    #await member.add_roles(welcomeRole)


#------------------------------------------------#
#           on voice server update               #
#------------------------------------------------#

@client.event
async def on_voice_state_update(member, before, after):
    serveur_id = member.guild.id

    with open('/home/Production/Qualia/server.json',"r") as f:
        data = json.load(f)
        f.close()

    category = client.get_channel(data[f"{serveur_id}"]["category"])

    #------------------------------------------------#
    #                Channel create                  #
    #------------------------------------------------#

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
                data[f"{serveur_id}"]["temp"][tempChannel.id] = member.id
            
                with open("/home/Production/Qualia/server.json", "w") as file:
                    json.dump(data, file, indent=4)
    
    #------------------------------------------------#
    #                Channel delete                  #
    #------------------------------------------------#
    deleteChannel = client.get_channel(before.channel.id)

    count = len(deleteChannel.members)

    for c in data[f"{serveur_id}"]["channel"]:
        for k, v in c.items():
            if (k == before.channel.name[1:]) and (count == 0) and (before.channel.id != v):
                await deleteChannel.delete()
                data[f"{serveur_id}"]["temp"].pop(f"{before.channel.id}")
                
                with open("/home/Production/Qualia/server.json", "w") as file:
                    json.dump(data, file, indent=4)

#------------------------------------------------#
#              on raw reaction add               #
#------------------------------------------------#

@client.event
async def on_raw_reaction_add(payload):
    conn = MysqlDef.connectionBDD()
    serveur_id = payload.guild_id

    messageReaction = MysqlDef.getMessageReaction(conn, serveur_id)

    for mr in messageReaction:
        msgInsc_id = mr[0]
        msgRole_id = mr[1]

    if (payload.message_id == msgInsc_id) and (payload.user_id != 863087982159724564):
        if payload.emoji.name == "📝":
            embed=discord.Embed(title="")
            embed.set_author(name="Qualia E-Sport", icon_url="https://zupimages.net/up/21/28/xrxs.png")
            embed.add_field(name="Réagissez à ce message par cette réaction pour commencer votre inscription.", value="📝")
            await payload.member.send(embed = embed)
    
    
    if (payload.message_id == msgRole_id) and (payload.user_id != 863087982159724564):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name = f"{payload.emoji.name}")
        if payload.event_type == "REACTION_ADD":
            await payload.member.add_roles(role)
            
@client.event
async def  on_raw_reaction_remove(payload):
    conn = MysqlDef.connectionBDD()
    serveur_id = payload.guild_id

    messageReaction = MysqlDef.getMessageReaction(conn, serveur_id)

    for mr in messageReaction:
        msgRole_id = mr[1]

    if (payload.message_id == msgRole_id) and (payload.user_id != 863087982159724564):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        member = discord.utils.get(guild.members, id=payload.user_id)
        role = discord.utils.get(guild.roles, name = f"{payload.emoji.name}")

        if payload.event_type == "REACTION_REMOVE":
            await member.remove_roles(role)





















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
    if ctx.author.id not in WHITELIST_IDS:
        await ctx.channel.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        conn = MysqlDef.connectionBDD()
        serveur_id = ctx.guild.id

        category = None

        category = await ctx.guild.create_category("Automatic Voice Channels", overwrites=None, reason=None)
        voiceChannelGénéral = await ctx.guild.create_voice_channel("🎧Général", user_limit=0, category = category)
        voiceChannelDuoQ = await ctx.guild.create_voice_channel("🎧DuoQ", user_limit=2, category = category)
        voiceChannelFlex = await ctx.guild.create_voice_channel("🎧Flex", user_limit=5, category = category)
        voiceChannel5v5 = await ctx.guild.create_voice_channel("🎧5 vs 5", user_limit=10, category = category)
        MysqlDef.setServerInfo(conn, serveur_id, category.id)
        
        with open('/home/Production/Qualia/server.json',"r") as f:
            data = json.load(f)
            f.close()
        
        data[serveur_id] = {}
        data[serveur_id]['category'] = category.id
        data[serveur_id]['channel'] = [{"Général" : voiceChannelGénéral.id},{"DuoQ" : voiceChannelDuoQ.id}, {"Flex" : voiceChannelFlex.id}, {"5 Vs 5" : voiceChannel5v5.id}]
        data[serveur_id]["temp"] = {}
        
        with open('/home/Production/Qualia/server.json','w') as f:
            json.dump(data, f, indent=4)
            f.close()


#--------------------------------------------------------------------#
#           Initialise le message de l'inscription lol               #
#--------------------------------------------------------------------#

@client.command()
async def initMessage(ctx):
    if ctx.author.id not in WHITELIST_IDS:
        await ctx.channel.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        conn = MysqlDef.connectionBDD()
        serveur_id = ctx.guild.id

        await ctx.message.delete()

        embed=discord.Embed(title="Vous souhaitez rejoindre une équipe ?")
        embed.set_author(name="Qualia E-Sport", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Réagissez à ce message par cette réaction pour commencer votre inscription.", value="📝")
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction("📝")

        MysqlDef.setMessageReaction(conn, serveur_id, msg.id)


#-------------------------------------------------------------#
#           Initialise le message des rôles lol               #
#-------------------------------------------------------------#

@client.command()
async def initMessageRole(ctx):
    if ctx.author.id not in WHITELIST_IDS:
        await ctx.channel.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        conn = MysqlDef.connectionBDD()
        serveur_id = ctx.guild.id

        await ctx.message.delete()

        embed=discord.Embed(title="Choisissez votre élo et votre lane !", color = discord.Color(0xFDFF00))
        embed.set_author(name="Qualia E-Sport", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Votre rang", value="> <:Iron:864174258594512926> **Iron**\n > <:Bronze:864174296681938985> **Bronze**\n > <:Silver:864174683213529099> **Silver**\n > <:Gold:864174707539181569> **Gold**\n > <:Platinum:864174739722862622> **Platinum**\n > <:Diamond:864174764212617216> **Diamond**\n > <:Master:864174782559813652> **Master**\n > <:GrandMaster:864174801194582056> **Grand Master**\n > <:Challenger:864174823760068608> **Challenger**\n", inline=False)
        embed.add_field(name="Votre poste", value="> <:Top:864176960493584455> **Top laner**\n > <:Jungle:864176942169325579> **Jungler**\n > <:Mid:864176925719134229> **Mid laner**\n > <:Adc:864176890692370472> **AD Carry**\n > <:Supp:864176867497476107> **Support**", inline=False)
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction("<:Iron:864174258594512926>")
        await msg.add_reaction("<:Bronze:864174296681938985>")
        await msg.add_reaction("<:Silver:864174683213529099>")
        await msg.add_reaction("<:Gold:864174707539181569>")
        await msg.add_reaction("<:Platinum:864174739722862622>")
        await msg.add_reaction("<:Diamond:864174764212617216>")
        await msg.add_reaction("<:Master:864174782559813652>")
        await msg.add_reaction("<:GrandMaster:864174801194582056>")
        await msg.add_reaction("<:Challenger:864174823760068608>")

        await msg.add_reaction("<:Top:864176960493584455>")
        await msg.add_reaction("<:Jungle:864176942169325579>")
        await msg.add_reaction("<:Mid:864176925719134229>")
        await msg.add_reaction("<:Adc:864176890692370472>")
        await msg.add_reaction("<:Supp:864176867497476107>")

        MysqlDef.setMessageRole(conn, serveur_id, msg.id)



client.run(TOKEN)