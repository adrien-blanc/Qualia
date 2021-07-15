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
import datetime

from math import *
from discord.ext import commands
from mysqlClass import MysqlDef
from messageClass import Message
from time import sleep
from riotwatcher import LolWatcher, ApiError # RIOT API


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
#            on raw reaction remove              #
#------------------------------------------------#

@client.event
async def  on_raw_reaction_remove(payload):
    conn = MysqlDef.connectionBDD()
    serveur_id = payload.guild_id

    messageReaction = MysqlDef.getMessageReaction(conn, serveur_id)

    for mr in messageReaction:
        msgInsc_id = mr[0]
        msgRole_id = mr[1]

    if (payload.message_id == msgInsc_id) and (payload.user_id != 863087982159724564):
        if payload.emoji.name == "📝":
            pass
            #await payload.member.dm_channel.purge()

    if (payload.message_id == msgRole_id) and (payload.user_id != 863087982159724564):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        member = discord.utils.get(guild.members, id=payload.user_id)
        role = discord.utils.get(guild.roles, name = f"{payload.emoji.name}")

        if payload.event_type == "REACTION_REMOVE":
            await member.remove_roles(role)
    
    

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

    if (payload.message_id == msgRole_id) and (payload.user_id != 863087982159724564):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name = f"{payload.emoji.name}")
        if payload.event_type == "REACTION_ADD":
            await payload.member.add_roles(role)

    #--------------------------------------------------#
    #              Procédure inscription               #
    #--------------------------------------------------#

    if (payload.message_id == msgInsc_id) and (payload.user_id != 863087982159724564):
        if payload.emoji.name == "📝":

            #-------------------------------------------#
            #              Procédure Init               #
            #-------------------------------------------#
            
            msgProcedure = await Message.confirmationInscription(payload.member)

            def checkEmoji(reaction, user):
                emoji_list = ["✅", "❌"]
                return payload.user_id == user.id and msgProcedure.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

            reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

            if reaction.emoji == "❌":
                await msgProcedure.delete()
                return
            else:

                #---------------------------------------------#
                #              Procédure Pseudo               #
                #---------------------------------------------#

                msgPseudo = await Message.inscriptionPseudo(payload.member)

                def check(m):
                    return m.author.id == payload.member.id and m.channel == payload.member.dm_channel

                try:
                    msgUser = await client.wait_for('message', timeout=300, check = check)
                except asyncio.TimeoutError:
                    await payload.member.send('Tu n\'as pas répondu dans les temps! Recommence la procédure depuis le début.')
                    await msgProcedure.delete()
                    await msgPseudo.delete()
                    return
                else:
                    pseudo = msgUser.content

                try:
                    me = lol_watcher.summoner.by_name(my_region, f"{pseudo}")
                    my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])

                    eloSolo = None
                    divSolo = None
                    eloFlex = None
                    divFlex = None

                    for i in range(len(my_ranked_stats)) : 
                        if my_ranked_stats[i]['queueType'] == "RANKED_SOLO_5x5":
                            eloSolo = my_ranked_stats[i]['tier']
                            divSolo = my_ranked_stats[i]['rank']
                        if my_ranked_stats[i]['queueType'] == "RANKED_FLEX_SR":
                            eloFlex = my_ranked_stats[i]['tier']
                            divFlex = my_ranked_stats[i]['rank']
                    
                    
                    msgConfirmation = await Message.confirmePseudo(payload.member, pseudo, eloSolo, divSolo, eloFlex, divFlex)

                    def checkEmoji(reaction, user):
                        emoji_list = ["✅", "❌"]
                        return payload.user_id == user.id and msgConfirmation.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                    reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                    if reaction.emoji == "❌":
                        await msgProcedure.delete()
                        await msgPseudo.delete()
                        await msgConfirmation.delete()
                        return

                except ApiError as error:
                    msgError = await Message.errorPseudo(payload.member)

                    await asyncio.sleep(10)
                    await msgError.delete()
                    await msgProcedure.delete()
                    await msgPseudo.delete()
                    await msgConfirmation.delete()
                    return
                

                #--------------------------------------------#
                #              Procédure Poste               #
                #--------------------------------------------#
                
                msgPoste = await Message.inscriptionPoste(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["<:Top:864176960493584455>", "<:Jungle:864176942169325579>", "<:Mid:864176925719134229>", "<:Adc:864176890692370472>", "<:Supp:864176867497476107>"]
                    return payload.user_id == user.id and msgPoste.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)
            
                msgTempo = await Message.inscriptionTempo(payload.member)

                guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
                role = discord.utils.get(guild.roles, name = f"{reaction.emoji.name}")
                
                await removeAllRolePoste(payload.member, guild)
                await payload.member.add_roles(role)

                poste = 0
                if reaction.emoji.name == "Top":
                    poste = 0
                elif reaction.emoji.name == "Jungle":
                    poste = 1
                elif reaction.emoji.name == "Mid":
                    poste = 2
                elif reaction.emoji.name == "Adc":
                    poste = 3
                elif reaction.emoji.name == "Supp":
                    poste = 4
                
                #---------------------------------------------------#
                #                    Calcul Div                     #
                #---------------------------------------------------#

                divTotal = 0

                guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
                
                elo = 0
                div = 0
                
                if eloSolo is None:
                    if eloFlex is None:
                        divTotal = 0
                    else:
                        role = discord.utils.get(guild.roles, name = f"{eloFlex.capitalize()}")
                        elo = await getElo(eloFlex.capitalize())
                        div = await getDiv(divFlex)
                        divTotal = await calculUserElo(elo, div)
                else:
                    role = discord.utils.get(guild.roles, name = f"{eloSolo.capitalize()}")
                    elo = await getElo(eloSolo.capitalize())
                    div = await getDiv(divSolo)
                    divTotal = await calculUserElo(elo, div)

                await removeAllRoleElo(payload.member, guild)
                await payload.member.add_roles(role)

                #---------------------------------------------------#
                #              Procédure Assossiation               #
                #---------------------------------------------------#
                await msgTempo.delete()
                msgChoix = await Message.inscriptionChoix(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["1️⃣", "2️⃣"]
                    return payload.user_id == user.id and msgChoix.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                try:
                    channelAdmin = client.get_channel(864909655259217940)
                    posteName = await getPosteName(poste)
                    eloName = await getEloName(elo)
                    divName = await getDivName(div)
                    if reaction.emoji == "1️⃣":
                        await Message.adminRecap(channelAdmin, payload.member.id, payload.member.name, me['id'], pseudo, posteName, eloName, divName, 1)
                        MysqlDef.setInfoUser(conn, payload.member.id, serveur_id, me['id'], pseudo, poste, divTotal, 0, 1)
                    elif reaction.emoji == "2️⃣":
                        await Message.adminRecap(channelAdmin, payload.member.id, payload.member.name, me['id'], pseudo, posteName, eloName, divName, 0)
                        MysqlDef.setInfoUser(conn, payload.member.id, serveur_id, me['id'], pseudo, poste, divTotal, 0, 0)
                except:
                    msgError = await Message.error(payload.member)

                    await asyncio.sleep(10)
                    await msgError.delete()
                    await msgProcedure.delete()
                    await msgPseudo.delete()
                    await msgPoste.delete()
                    await msgChoix.delete()
                    await msgConfirmation.delete()
                    return

                await msgProcedure.delete()
                await msgPseudo.delete()
                await msgPoste.delete()
                await msgChoix.delete()
                await msgConfirmation.delete()
                
                msgFin = await Message.inscriptionFin(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["✅"]
                    return payload.user_id == user.id and msgFin.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                if reaction.emoji == "✅":
                    await msgFin.delete()
            




























#------------------------------------------------#
#                                                #
#              Commandes Globales                #
#                                                #
#------------------------------------------------#

#-------------------------------------------#
#           Purge one channel               #
#-------------------------------------------#

@client.command()
async def purge(ctx):
    await ctx.channel.purge()




















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

























#------------------------------------------------#
#                                                #
#               Fonctions Glbales                #
#                                                #
#------------------------------------------------#

#------------------------------------------------#
#              Set Team Creation                 #
#------------------------------------------------#
async def setTeamCreation(bool):
    conn = MysqlDef.connectionBDD()

    MysqlDef.setTeamCrea(conn, bool)

    conn.close()

#------------------------------------------------#
#              Get Team Creation                 #
#------------------------------------------------#
async def getTeamCreation():
    conn = MysqlDef.connectionBDD()

    gets = MysqlDef.getTeamCrea(conn)

    check = 1
    for get in gets :
        check = get[0]

    conn.close()

    return check

#------------------------------------------------#
#                Calcul User Elo                 #
#------------------------------------------------#
async def calculUserElo(userElo, userDiv):

    calculTotalDiv = (userElo * 4) + (4 - userDiv)

    return calculTotalDiv

#------------------------------------------------#
#            Calcul Inverse User Elo             #
#------------------------------------------------#
async def calculInvUserElo(userDiv):
    calculDiv = (4-(userDiv%4))
    calculElo = floor(userDiv/4)

    return calculElo,calculDiv

#------------------------------------------------#
#                 Get Poste User                 #
#------------------------------------------------#
async def getPosteName(poste):
    poste_name = ""
    if int(poste) == 0:
        poste_name = "TOP"
    elif int(poste) == 1:
        poste_name = "JGL"
    elif int(poste) == 2:
        poste_name = "MID"
    elif int(poste) == 3:
        poste_name = "ADC"
    elif int(poste) == 4:
        poste_name = "SUPP"
    
    return poste_name

#------------------------------------------------#
#               Get Elo User (int)               #
#------------------------------------------------#
async def getElo(elo_name):
    elo = 0
    if elo_name == "Iron":
        elo = 0
    elif elo_name == "Bronze":
        elo = 1
    elif elo_name == "Silver":
        elo = 2
    elif elo_name == "Gold":
        elo = 3
    elif elo_name == "Platinum":
        elo = 4
    elif elo_name == "Diamond":
        elo = 5
    elif elo_name == "Master":
        elo = 6
    elif elo_name == "Grandmaster":
        elo = 7
    elif elo_name == "Challenger":
        elo = 8

    return elo

async def getDiv(elo_div):
    div = 0
    if elo_div == "I":
        div = 1
    elif elo_div == "II":
        div = 2
    elif elo_div == "III":
        div = 3
    elif elo_div == "IV":
        div = 4
    return div

#------------------------------------------------#
#               Get Elo User (str)               #
#------------------------------------------------#
async def getEloName(elo):
    elo_name = ""
    if elo == 0:
        elo_name = "Iron"
    elif elo == 1:
        elo_name = "Bronze"
    elif elo == 2:
        elo_name = "Silver"
    elif elo == 3:
        elo_name = "Gold"
    elif elo == 4:
        elo_name = "Platinum"
    elif elo == 5:
        elo_name = "Diamond"
    elif elo == 6:
        elo_name = "Master"
    elif elo == 7:
        elo_name = "GrandMaster"
    elif elo == 8:
        elo_name = "Challenger"
    return elo_name

async def getDivName(div):
    divReturn = 0
    if div == 1:
        divReturn = "I"
    elif div == 2:
        divReturn = "II"
    elif div == 3:
        divReturn = "III"
    elif div == 4:
        divReturn = "IV"
    return divReturn


#------------------------------------------------#
#                  Remove Role                   #
#------------------------------------------------#

async def removeAllRolePoste(member, guild):
    role_top = discord.utils.get(guild.roles, name = 'Top')
    role_jungle = discord.utils.get(guild.roles, name = 'Jungle')
    role_mid = discord.utils.get(guild.roles, name = 'Mid')
    role_adc = discord.utils.get(guild.roles, name = 'Adc')
    role_support = discord.utils.get(guild.roles, name = 'Supp')

    
    if role_top in member.roles:
        await member.remove_roles(role_top)
    if role_jungle in member.roles:
        await member.remove_roles(role_jungle)
    if role_mid in member.roles:
        await member.remove_roles(role_mid)
    if role_adc in member.roles:
        await member.remove_roles(role_adc)
    if role_support in member.roles:
        await member.remove_roles(role_support)

#------------------------------------------------#
#                   Remove Elo                   #
#------------------------------------------------#

async def removeAllRoleElo(member, guild):

    role_iron = discord.utils.get(guild.roles, name = 'Iron')
    role_bronze = discord.utils.get(guild.roles, name = 'Bronze')
    role_silver = discord.utils.get(guild.roles, name = 'Silver')
    role_gold = discord.utils.get(guild.roles, name = 'Gold')
    role_platinum = discord.utils.get(guild.roles, name = 'Platinum')
    role_diamond = discord.utils.get(guild.roles, name = 'Diamond')
    role_master = discord.utils.get(guild.roles, name = 'Master')
    role_grandmaster = discord.utils.get(guild.roles, name = 'GrandMaster')
    role_challenger = discord.utils.get(guild.roles, name = 'Challenger')

    if role_iron in member.roles:
        await member.remove_roles(role_iron)
    if role_bronze in member.roles:
        await member.remove_roles(role_bronze)
    if role_silver in member.roles:
        await member.remove_roles(role_silver)
    if role_gold in member.roles:
        await member.remove_roles(role_gold)
    if role_platinum in member.roles:
        await member.remove_roles(role_platinum)
    if role_diamond in member.roles:
        await member.remove_roles(role_diamond)
    if role_master in member.roles:
        await member.remove_roles(role_master)
    if role_grandmaster in member.roles:
        await member.remove_roles(role_grandmaster)
    if role_challenger in member.roles:
        await member.remove_roles(role_challenger)




















#------------------------------------------------#
#                                                #
#                Commande crontab                #
#                                                #
#------------------------------------------------#

#--------------------------------------------------------------------#
#           Check de la disponibilité de l'API de Riot               #
#--------------------------------------------------------------------#
"""
Cette fonction test la disponiblité de l'API de Riot
dans le cas où elle n'est plus accessible, 
elle m'envoie en message privé un message pour me prévenir.
"""

@aiocron.crontab('0/5 * * * *')
async def checkAPI():
    user = client.get_user(211153408709754880)
    now = datetime.datetime.now()
    print(f" CHECK API : {now}")

    try:
        me = lol_watcher.summoner.by_name(my_region, f"{user}")
        my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
    except ApiError as error:
        await user.send(f"La clé d'API Riot n'est pas accessible. | {error} | https://developer.riotgames.com/")      
        return


client.run(TOKEN)