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
import sys

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
#                on member message               #
#------------------------------------------------#
"""
@client.event
async def on_message(message):
    channel = client.get_channel(867702043690270750)
    conn = MysqlDef.connectionBDD()
    check = MysqlDef.checkdot(conn)

    for c in check:
        verif = c[0]
    if ('.' in message.content.lower() and message.channel.id == channel.id and verif == 0 and message.author.id != 863087982159724564) :
        await message.channel.send("Le prochain qui envoie un point dans ce channel je le ban.")
        MysqlDef.setcheckdot(conn)

    if ('.' in message.content.lower() and message.channel.id == channel.id and verif == 1 and message.author.id != 863087982159724564) :
        await message.author.ban()
        await message.channel.send(f"**{message.author}** a été banni.")

    conn.close()
"""
"""
@client.event
async def on_message(message):
    channel = client.get_channel(804097189081120768)

    

    if message.channel.id == channel.id:

        with open('/home/Production/Qualia/giveaway.json',"r") as f:
            data = json.load(f)
            f.close()

        members = data["members"]


        if (str(message.author.id) in members and message.author.id != 863087982159724564):
            await message.delete()
            await channel.send("{} tu as déjà participé !".format(message.author))
        elif(message and message.author.id != 863087982159724564):
            await channel.send("**{}** a gagné ! Le jeu est terminé.".format(message.author))
        elif (message.author.id != 863087982159724564) :
            data["members"][message.author.id] = message.author.id
            with open("/home/Production/Qualia/giveaway.json", "w") as file:
                json.dump(data, file, indent=4)
"""

@client.command(brief="")
async def setGiveaway(ctx, answer = None, word = None, price = None):
    if ((answer is None) or (word is None) or (price is None)):
        await ctx.channel.send("Respecter ce format : !setGiveaway \"my question (string)\" \"my answer (string)\" \"price (integer)\" ")
    else:
        await ctx.channel.send(f"{answer} {word} {price}")
        
#------------------------------------------------#
#                on member join                  #
#------------------------------------------------#

@client.event
async def on_member_join(member):
    welcomeRole = discord.utils.get(member.guild.roles,name="Qualia") # Add spécifique rôle when member arive on serve.
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
    if payload.guild_id is None:
        serveur_id = 862779743882313748 # Serveur de Dev
    else: 
        serveur_id = payload.guild_id

    messageReaction = MysqlDef.getMessageReaction(conn, serveur_id)

    for mr in messageReaction:
        msgRole_id = mr[1]
        msgRoleJeu_id = mr[3]



    if (payload.message_id == msgRole_id) and (payload.user_id != 863087982159724564):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        member = discord.utils.get(guild.members, id=payload.user_id)
        role = discord.utils.get(guild.roles, name = f"{payload.emoji.name}")

        if payload.event_type == "REACTION_REMOVE":
            await member.remove_roles(role)

    if (payload.message_id == msgRoleJeu_id) and (payload.user_id != 863087982159724564):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        member = discord.utils.get(guild.members, id=payload.user_id)
        role = None
        
        if payload.emoji.name == "LeagueofLegends":
            role = discord.utils.get(guild.roles, name = "League of Legends")
        elif payload.emoji.name == "Valorant":
            role = discord.utils.get(guild.roles, name = "Valorant")
        elif payload.emoji.name == "TFT":
            role = discord.utils.get(guild.roles, name = "TFT")
        elif payload.emoji.name == "CSGO":
            role = discord.utils.get(guild.roles, name = "CS:GO")
        elif payload.emoji.name == "RocketLeague":
            role = discord.utils.get(guild.roles, name = "Rocket League")
        elif payload.emoji.name == "Hearthstone":
            role = discord.utils.get(guild.roles, name = "Hearthstone")
        elif payload.emoji.name == "Chess":
            role = discord.utils.get(guild.roles, name = "Chess")
        await member.remove_roles(role)

    conn.close()
    
    

#------------------------------------------------#
#              on raw reaction add               #
#------------------------------------------------#

@client.event
async def on_raw_reaction_add(payload):
    conn = MysqlDef.connectionBDD()
    if payload.guild_id is None:
        serveur_id = 862779743882313748 # Serveur de Dev
    else: 
        serveur_id = payload.guild_id
    guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)

    messageReaction = MysqlDef.getMessageReaction(conn, serveur_id)

    for mr in messageReaction:
        msgInsc_id = mr[0]
        msgRole_id = mr[1]
        msgMentorat_id = mr[2]
        msgRoleJeu_id = mr[3]

    if (payload.message_id == msgRole_id) and (payload.user_id != 863087982159724564):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        role = discord.utils.get(guild.roles, name = f"{payload.emoji.name}")
        if payload.event_type == "REACTION_ADD":
            await payload.member.add_roles(role)

        
    
    if (payload.message_id == msgRoleJeu_id) and (payload.user_id != 863087982159724564):
        guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
        role = None
        if payload.emoji.name == "LeagueofLegends":
            role = discord.utils.get(guild.roles, name = "League of Legends")
        elif payload.emoji.name == "Valorant":
            role = discord.utils.get(guild.roles, name = "Valorant")
        elif payload.emoji.name == "TFT":
            role = discord.utils.get(guild.roles, name = "TFT")
        elif payload.emoji.name == "CSGO":
            role = discord.utils.get(guild.roles, name = "CS:GO")
        elif payload.emoji.name == "RocketLeague":
            role = discord.utils.get(guild.roles, name = "Rocket League")
        elif payload.emoji.name == "Hearthstone":
            role = discord.utils.get(guild.roles, name = "Hearthstone")
        elif payload.emoji.name == "Chess":
            role = discord.utils.get(guild.roles, name = "Chess")
        
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
                conn.close()
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
                    conn.close()
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
                    
                    
                    msgConfirmation = await Message.confirmePseudoMentor(payload.member, pseudo, eloSolo, divSolo, eloFlex, divFlex)

                    def checkEmoji(reaction, user):
                        emoji_list = ["✅", "❌"]
                        return payload.user_id == user.id and msgConfirmation.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                    reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                    if reaction.emoji == "❌":
                        await msgProcedure.delete()
                        await msgPseudo.delete()
                        await msgConfirmation.delete()
                        conn.close()
                        return

                except ApiError as error:
                    
                    msgError = await Message.errorPseudo(payload.member, error)

                    await asyncio.sleep(10)
                    await msgError.delete()
                    await msgProcedure.delete()
                    await msgPseudo.delete()
                    await msgConfirmation.delete()
                    conn.close()
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

                msgChoix = await Message.inscriptionChoix(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["1️⃣", "2️⃣"]
                    return payload.user_id == user.id and msgChoix.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                try:
                    channelAdmin = client.get_channel(864909655259217940)
                    channelRecap = client.get_channel(867768457171566612)
                    posteName = await getPosteName(poste)
                    eloName = await getEloName(elo)
                    divName = await getDivName(div)
                    if reaction.emoji == "1️⃣":
                        await Message.adminRecap(channelAdmin, payload.member.id, payload.member.name, me['id'], pseudo, posteName, eloName, divName, 1)
                        await Message.Recap(channelRecap, payload.member.name, pseudo, posteName, eloSolo, divSolo, eloFlex, divFlex, divName, 1)
                        MysqlDef.setInfoUser(conn, payload.member.id, serveur_id, me['id'], pseudo, poste, divTotal, 0, 1)
                    elif reaction.emoji == "2️⃣":
                        await Message.adminRecap(channelAdmin, payload.member.id, payload.member.name, me['id'], pseudo, posteName, eloName, divName, 0)
                        await Message.Recap(channelRecap, payload.member.name, pseudo, posteName, eloSolo, divSolo, eloFlex, divFlex, divName, 0)
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
                    conn.close()
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
    
    #-----------------------------------------------#
    #              Procédure Mentorat               #
    #-----------------------------------------------#

    if (payload.message_id == msgMentorat_id) and (payload.user_id != 863087982159724564):
        if payload.emoji.name == "👨🏽‍🏫":

            msgInscr = await Message.mentorInit(payload.member)

            def checkEmoji(reaction, user):
                emoji_list = ["✅", "❌"]
                return payload.user_id == user.id and msgInscr.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

            reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

            if reaction.emoji == "❌":
                await msgInscr.delete()
                conn.close()
                return
            else:

                #---------------------------------------------#
                #              Procédure Pseudo               #
                #---------------------------------------------#

                msgPseudo = await Message.mentorPseudo(payload.member)

                def check(m):
                    return m.author.id == payload.member.id and m.channel == payload.member.dm_channel

                try:
                    msgUser = await client.wait_for('message', timeout=300, check = check)
                except asyncio.TimeoutError:
                    await payload.member.send('Tu n\'as pas répondu dans les temps! Recommence la procédure depuis le début.')
                    await msgInscr.delete()
                    await msgPseudo.delete()
                    conn.close()
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
                    
                    
                    msgConfirmation = await Message.confirmePseudoMentor(payload.member, pseudo, eloSolo, divSolo, eloFlex, divFlex)

                    def checkEmoji(reaction, user):
                        emoji_list = ["✅", "❌"]
                        return payload.user_id == user.id and msgConfirmation.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                    reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                    if reaction.emoji == "❌":
                        await msgInscr.delete()
                        await msgPseudo.delete()
                        await msgConfirmation.delete()
                        conn.close()
                        return

                except ApiError as error:
                    msgError = await Message.errorPseudo(payload.member)

                    await asyncio.sleep(10)
                    await msgError.delete()
                    await msgInscr.delete()
                    await msgPseudo.delete()
                    await msgConfirmation.delete()
                    conn.close()
                    return

                #--------------------------------------------#
                #              Procédure Poste               #
                #--------------------------------------------#
                
                msgPoste = await Message.mentorPoste(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["<:Top:864176960493584455>", "<:Jungle:864176942169325579>", "<:Mid:864176925719134229>", "<:Adc:864176890692370472>", "<:Supp:864176867497476107>"]
                    return payload.user_id == user.id and msgPoste.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

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

                #--------------------------------------------#
                #              Procédure Nombre              #
                #--------------------------------------------#
                
                msgNombre = await Message.mentorNombre(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
                    return payload.user_id == user.id and msgNombre.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)


                nbr = 1
                if reaction.emoji == "1️⃣":
                    nbr = 1
                elif reaction.emoji == "2️⃣":
                    nbr = 2
                elif reaction.emoji == "3️⃣":
                    nbr = 3
                elif reaction.emoji == "4️⃣":
                    nbr = 4
                elif reaction.emoji == "5️⃣":
                    nbr = 5
                elif reaction.emoji == "6️⃣":
                    nbr = 6
                elif reaction.emoji == "7️⃣":
                    nbr = 7
                elif reaction.emoji == "8️⃣":
                    nbr = 8
                elif reaction.emoji == "9️⃣":
                    nbr = 9

                
                #-----------------------------------------------#
                #              Procédure Pedagogue              #
                #-----------------------------------------------#
                
                msgPeda = await Message.mentorPeda(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["✅", "➕", "❌"]
                    return payload.user_id == user.id and msgPeda.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                peda = 0
                if reaction.emoji == "✅":
                    peda = 2
                elif reaction.emoji == "➕":
                    peda = 1
                elif reaction.emoji == "❌":
                    peda = 0

                #-------------------------------------------------#
                #              Procédure Micro/Macro              #
                #-------------------------------------------------#
                
                msgMicroMacro = await Message.mentorMicroMacro(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["0️⃣", "1️⃣", "2️⃣"]
                    return payload.user_id == user.id and msgMicroMacro.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                style = 0
                if reaction.emoji == "0️⃣":
                    style = 0
                elif reaction.emoji == "1️⃣":
                    style = 1
                elif reaction.emoji == "2️⃣":
                    style = 2

                #-------------------------------------------------#
                #              Inscription du mentor              #
                #-------------------------------------------------#

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
                
                MysqlDef.addMentor(conn, payload.member.id, serveur_id, me['id'], pseudo, divTotal, poste, nbr, peda, style)
                
                channels = MysqlDef.getMentorChannels(conn, serveur_id)

                posteName = await getPosteName(poste)

                eloName = await getEloName(elo)
                divName = await getDivName(div)

                for channel in channels:
                    chan = client.get_channel(channel[0])
                    
                    msgMentor = await Message.newMentor(chan, payload.member.name,  pseudo, eloName, divName, posteName, nbr, style)


                role = discord.utils.get(guild.roles, name = 'mentor')
                await payload.member.add_roles(role)

                msgFin = await Message.mentorFin(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["✅"]
                    return payload.user_id == user.id and msgFin.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                if reaction.emoji == "✅":
                    await msgFin.delete()

                with open('/home/Production/Qualia/server.json',"r") as f:
                    data = json.load(f)
                    f.close()

                data[f"{serveur_id}"]["mentor"][msgMentor.id] = payload.member.id
            
                with open("/home/Production/Qualia/server.json", "w") as file:
                    json.dump(data, file, indent=4)

                
                


        if payload.emoji.name == "📚":
            msgInit = await Message.studentInit(payload.member)

            def checkEmoji(reaction, user):
                emoji_list = ["✅", "❌"]
                return payload.user_id == user.id and msgInit.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

            reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

            if reaction.emoji == "❌":
                await msgInscr.delete()
                conn.close()
                return
            else:

                #---------------------------------------------#
                #              Procédure Pseudo               #
                #---------------------------------------------#

                msgPseudo = await Message.studentPseudo(payload.member)

                def check(m):
                    return m.author.id == payload.member.id and m.channel == payload.member.dm_channel

                try:
                    msgUser = await client.wait_for('message', timeout=300, check = check)
                except asyncio.TimeoutError:
                    await payload.member.send('Tu n\'as pas répondu dans les temps! Recommence la procédure depuis le début.')
                    await msgInscr.delete()
                    await msgPseudo.delete()
                    conn.close()
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
                    
                    
                    msgConfirmation = await Message.confirmePseudostudent(payload.member, pseudo, eloSolo, divSolo, eloFlex, divFlex)

                    def checkEmoji(reaction, user):
                        emoji_list = ["✅", "❌"]
                        return payload.user_id == user.id and msgConfirmation.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                    reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                    if reaction.emoji == "❌":
                        await msgInscr.delete()
                        await msgPseudo.delete()
                        await msgConfirmation.delete()
                        conn.close()
                        return

                except ApiError as error:
                    msgError = await Message.errorPseudo(payload.member)

                    await asyncio.sleep(10)
                    await msgError.delete()
                    await msgInscr.delete()
                    await msgPseudo.delete()
                    await msgConfirmation.delete()
                    conn.close()
                    return

                #--------------------------------------------#
                #              Procédure Poste               #
                #--------------------------------------------#
                
                msgPoste = await Message.studentPoste(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["<:Top:864176960493584455>", "<:Jungle:864176942169325579>", "<:Mid:864176925719134229>", "<:Adc:864176890692370472>", "<:Supp:864176867497476107>"]
                    return payload.user_id == user.id and msgPoste.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

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

                

                #-------------------------------------------#
                #              Procédure Debat              #
                #-------------------------------------------#
                
                msgDebat = await Message.studentDebat(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["0️⃣", "1️⃣"]
                    return payload.user_id == user.id and msgDebat.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)


                debat = 0
                if reaction.emoji == "0️⃣":
                    debat = 1
                elif reaction.emoji == "1️⃣":
                    debat = 0

                

                #-----------------------------------------------#
                #              Procédure Apprendre              #
                #-----------------------------------------------#

                msgAppendre = await Message.studentApprendre(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["0️⃣", "1️⃣"]
                    return payload.user_id == user.id and msgAppendre.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)


                apprendre = 0
                if reaction.emoji == "0️⃣":
                    apprendre = 0
                elif reaction.emoji == "1️⃣":
                    apprendre = 1


                #-------------------------------------------#
                #              Procédure Style              #
                #-------------------------------------------#

                msgStyle = await Message.studentStyle(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["0️⃣", "1️⃣", "2️⃣"]
                    return payload.user_id == user.id and msgStyle.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)


                style = 0
                if reaction.emoji == "0️⃣":
                    style = 0
                elif reaction.emoji == "1️⃣":
                    style = 1
                elif reaction.emoji == "2️⃣":
                    style = 2

                MysqlDef.setEleveInfo(conn, payload.member.id, serveur_id, me['id'], pseudo, poste, debat, apprendre, style)

                channels = MysqlDef.getMentorChannels(conn, serveur_id)

                posteName = await getPosteName(poste)

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

                eloName = await getEloName(elo)
                divName = await getDivName(div)

                for channel in channels:
                    chan = client.get_channel(channel[1])
                    
                    msgNewStudent = await Message.newStudent(chan, payload.member.name,  pseudo, eloName, divName, posteName, debat, apprendre, style)


                role = discord.utils.get(guild.roles, name = 'élève')
                await payload.member.add_roles(role)

                msgFin = await Message.mentorFin(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["✅"]
                    return payload.user_id == user.id and msgFin.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                if reaction.emoji == "✅":
                    await msgFin.delete()

                with open('/home/Production/Qualia/server.json',"r") as f:
                    data = json.load(f)
                    f.close()

                data[f"{serveur_id}"]["student"][msgNewStudent.id] = payload.member.id
            
                with open("/home/Production/Qualia/server.json", "w") as file:
                    json.dump(data, file, indent=4)


    with open('/home/Production/Qualia/server.json',"r") as f:
        data = json.load(f)
        f.close()
                
    for c in data[f"{serveur_id}"]["mentor"]:
        if str(payload.message_id) == c:
            check = MysqlDef.checkEleveExist(conn, payload.member.id, serveur_id)
            for ch in check:
                if ch[0] == 0:
                    await payload.member.send("Vous devez vous inscrire en tant qu'élève pour pouvoir choisir un mentor.")
                    return

            infos = MysqlDef.getEleveInfo(conn, payload.member.id, serveur_id)

            for info in infos:
                riot_id = info[2]
                pseudo = info[3]
                poste = await getPosteName(info[4])
                debat = info[5]
                apprendre = await getInfo(info[6])
                style = info[7]

            my_ranked_stats = lol_watcher.league.by_summoner(my_region, riot_id)

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
            
            mentor = guild.get_member(int(data[f"{serveur_id}"]["mentor"][c]))

            msgMentor = await Message.studentInfo(mentor, payload.member, pseudo, eloSolo, divSolo, eloFlex, divFlex, poste, debat, apprendre, style)

            def checkEmoji(reaction, user):
                emoji_list = ["✅","❌"]
                return mentor.id == user.id and msgMentor.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

            reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

            if reaction.emoji == "❌":
                await Message.studentRefus(payload.member)
            elif reaction.emoji == "✅":
                
                channels = MysqlDef.getMentorat(conn, serveur_id)

                for chan in channels:
                    channelMentor = guild.get_channel(chan[2])
                    channelStudent = guild.get_channel(chan[3])

                with open('/home/Production/Qualia/server.json',"r") as f:
                    data = json.load(f)
                    f.close()

                for c in data[f"{serveur_id}"]["student"]:
                    if payload.member.id == data[f"{serveur_id}"]["student"][c]:
                        msgToDelete = await channelStudent.fetch_message(c)
                        await msgToDelete.delete()
                        data[f"{serveur_id}"]["student"].pop(f"{c}")
                        break

                msgToDelete = await channelMentor.fetch_message(payload.message_id)
                data[f"{serveur_id}"]["mentor"].pop(f"{payload.message_id}")
                await msgToDelete.delete()
                with open("/home/Production/Qualia/server.json", "w") as file:
                    json.dump(data, file, indent=4)
                

                await Message.studentAccept(payload.member)
                categorie = MysqlDef.getCategoriMentor(conn, serveur_id)
                for cate in categorie:
                    category = guild.get_channel(cate[0])

                roleMentor = discord.utils.get(guild.roles, name="mentor")
                roleEleve = discord.utils.get(guild.roles, name="élève")
                roleLol = discord.utils.get(guild.roles, name="League of Legends")

                channelGeneral = await guild.create_text_channel(f"☕𝐆𝐞́𝐧𝐞́𝐫𝐚𝐥-{payload.member.name}", category = category)
                await channelGeneral.set_permissions(payload.member, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=True, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(mentor, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = True, embed_links=True, use_slash_commands=False, mute_members=True, deafen_members=False, move_members=True, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(roleMentor, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(roleEleve, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(roleLol, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(guild.default_role, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                
                voiceChannel = await guild.create_voice_channel(f"🎧𝐆𝐞́𝐧𝐞́𝐫𝐚𝐥-{payload.member.name}", category = category)
                await voiceChannel.set_permissions(payload.member, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=True, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(mentor, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = True, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = True, embed_links=True, use_slash_commands=False, mute_members=True, deafen_members=False, move_members=True, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(roleMentor, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(roleEleve, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(roleLol, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(guild.default_role, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)


    with open('/home/Production/Qualia/server.json',"r") as f:
        data = json.load(f)
        f.close()
                
    for c in data[f"{serveur_id}"]["student"]:
        if str(payload.message_id) == c:
            check = MysqlDef.checkMentorExist(conn, payload.member.id, serveur_id)
            for ch in check:
                if ch[0] == 0:
                    await payload.member.send("Vous devez vous inscrire en tant que mentor pour pouvoir choisir un élève.")
                    return

            infos = MysqlDef.getMentorInfo(conn, payload.member.id, serveur_id) #`discord_id`, `server_id`, `riot_id`, `pseudo`, `poste`, `micromacro`

            for info in infos:
                riot_id = info[2]
                pseudo = info[3]
                poste = await getPosteName(info[4])
                style = info[5]

            my_ranked_stats = lol_watcher.league.by_summoner(my_region, riot_id)

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
            
            student = guild.get_member(int(data[f"{serveur_id}"]["student"][c]))

            msgStudent = await Message.mentorInfo(student, payload.member, pseudo, eloSolo, divSolo, eloFlex, divFlex, poste, style)

            def checkEmoji(reaction, user):
                emoji_list = ["✅","❌"]
                return student.id == user.id and msgStudent.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

            reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

            if reaction.emoji == "❌":
                await Message.mentorRefus(payload.member)
            elif reaction.emoji == "✅":
                
                channels = MysqlDef.getMentorat(conn, serveur_id)

                for chan in channels:
                    channelMentor = guild.get_channel(chan[2])
                    channelStudent = guild.get_channel(chan[3])

                with open('/home/Production/Qualia/server.json',"r") as f:
                    data = json.load(f)
                    f.close()

                for c in data[f"{serveur_id}"]["mentor"]:
                    if payload.member.id == data[f"{serveur_id}"]["mentor"][c]:
                        msgToDelete = await channelMentor.fetch_message(c)
                        await msgToDelete.delete()
                        data[f"{serveur_id}"]["mentor"].pop(f"{c}")
                        break

                msgToDelete = await channelStudent.fetch_message(payload.message_id)
                data[f"{serveur_id}"]["student"].pop(f"{payload.message_id}")
                await msgToDelete.delete()
                with open("/home/Production/Qualia/server.json", "w") as file:
                    json.dump(data, file, indent=4)
                

                await Message.mentorAccept(payload.member)
                categorie = MysqlDef.getCategoriMentor(conn, serveur_id)
                for cate in categorie:
                    category = guild.get_channel(cate[0])

                roleMentor = discord.utils.get(guild.roles, name="mentor")
                roleEleve = discord.utils.get(guild.roles, name="élève")
                roleLol = discord.utils.get(guild.roles, name="League of Legends")

                channelGeneral = await guild.create_text_channel(f"☕𝐆𝐞́𝐧𝐞́𝐫𝐚𝐥-{student.name}", category = category)
                await channelGeneral.set_permissions(student, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=True, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(payload.member, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = True, embed_links=True, use_slash_commands=False, mute_members=True, deafen_members=False, move_members=True, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(roleMentor, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(roleEleve, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(roleLol, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await channelGeneral.set_permissions(guild.default_role, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                
                voiceChannel = await guild.create_voice_channel(f"🎧𝐆𝐞́𝐧𝐞́𝐫𝐚𝐥-{student.name}", category = category)
                await voiceChannel.set_permissions(student, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=True, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(payload.member, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = True, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = True, embed_links=True, use_slash_commands=False, mute_members=True, deafen_members=False, move_members=True, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(roleMentor, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(roleEleve, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(roleLol, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
                await voiceChannel.set_permissions(guild.default_role, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
    conn.close()
            




























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
    if ctx.author.id not in WHITELIST_IDS:
        await ctx.channel.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        await ctx.channel.purge()

#---------------------------------------#
#           Delete mentor               #
#---------------------------------------#

@client.command()
async def deleteMentor(ctx, person : discord.Member = None):
    if ctx.author.id not in WHITELIST_IDS:
        await ctx.channel.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        if person is None:
            await ctx.send("Vous n'avez pas renseigné le joueur.")
        else:
            conn = MysqlDef.connectionBDD()
            server_id = ctx.guild.id
            MysqlDef.deleteMentor(conn, person.id, server_id)
            roleMentor = discord.utils.get(ctx.guild.roles, name="mentor")
            await person.remove_roles(roleMentor)
            await ctx.channel.send(f"{person.name} a bien été retiré des mentors.")

#----------------------------------------#
#           Delete student               #
#----------------------------------------#

@client.command()
async def deleteStudent(ctx, person : discord.Member = None):
    if ctx.author.id not in WHITELIST_IDS:
        await ctx.channel.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        if person is None:
            await ctx.send("Vous n'avez pas renseigné le joueur.")
        else:
            conn = MysqlDef.connectionBDD()
            server_id = ctx.guild.id
            MysqlDef.deleteStudent(conn, person.id, server_id)
            roleStudent = discord.utils.get(ctx.guild.roles, name="élève")
            await person.remove_roles(roleStudent)
            await ctx.channel.send(f"{person.name} a bien été retiré des élèves.")



#-------------------------------------------#
#                Create Team                #
#-------------------------------------------#

@client.command()
async def createTeam(ctx):
    if ctx.author.id not in WHITELIST_IDS:
        await ctx.channel.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        msgWait = await Message.waitTeam(ctx.channel)

        serveur_id = ctx.guild.id

        check = await getTeamCreation()
        while check == 1 :
            number = random.randrange(10)
            await asyncio.sleep(number)
            check = await getTeamCreation()

        await setTeamCreation(1)

        conn = MysqlDef.connectionBDD()

        next_id = MysqlDef.getNextTeamId(conn)

        team_id = None
        compteur = 1
        compteurNextId = 0
        next_id_len = len(next_id)
        while team_id is None:
            if (compteurNextId == next_id_len and team_id is None):
                team_id = compteur
            else:
                if next_id[compteurNextId][0] != compteur:
                    team_id = compteur
                compteur += 1
                compteurNextId += 1

        name_team = f"Team-{team_id}"

        #------------------------------------------------#
        #                      Role                      #
        #------------------------------------------------#
        if not (discord.utils.get(ctx.guild.roles, name=name_team)):
            role = await ctx.guild.create_role(name=name_team)
            randomColor = random.randint(0x888888, 0xbbbbbb)
            await role.edit(hoist = True, mentionable = True, colour = randomColor, positions=31)
        else:
            role = discord.utils.get(ctx.guild.roles, name =name_team)

        #------------------------------------------------#
        #                     Category                   #
        #------------------------------------------------#
        category = await ctx.guild.create_category(name_team, overwrites=None, reason=None)

        roleDevAdmin = discord.utils.get(ctx.guild.roles, name="Pôle développement")
        roleTeamAdmin = discord.utils.get(ctx.guild.roles, name="Pôle communication")
        roleCoach = discord.utils.get(ctx.guild.roles, name="Coach/Analyste")
        roleManager = discord.utils.get(ctx.guild.roles, name="Manager")

        await category.set_permissions(role, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=True, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
        await category.set_permissions(roleDevAdmin, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = True, mention_everyone = True, read_message_history = True, manage_channels = True, manage_permissions = True, manage_webhooks = True, create_instant_invite = True, manage_messages = True, embed_links=True,  use_slash_commands=True, mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, stream=True, priority_speaker=True, send_tts_messages=True)
        await category.set_permissions(roleTeamAdmin, read_messages=True, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = True, mention_everyone = True, read_message_history = True, manage_channels = True, manage_permissions = True, manage_webhooks = True, create_instant_invite = True, manage_messages = True, embed_links=True, use_slash_commands=True, mute_members=True, deafen_members=True, move_members=True, use_voice_activation=True, stream=True, priority_speaker=True, send_tts_messages=True)
        await category.set_permissions(roleManager,  read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False,  use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
        await category.set_permissions(roleCoach, read_messages=False, send_messages=True, connect=True, speak=True, add_reactions = True, attach_files = True, external_emojis = False, mention_everyone = True, read_message_history = True, manage_channels = True, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = True, embed_links=True, use_slash_commands=False, mute_members=True, deafen_members=False, move_members=True, use_voice_activation=True, stream=True, priority_speaker=True, send_tts_messages=False)
        await category.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)


        #------------------------------------------------#
        #                    Channel                     #
        #------------------------------------------------#

        channelOpgg = await ctx.guild.create_text_channel('📝𝐨𝐩𝐠𝐠', category=category)
        await channelOpgg.set_permissions(roleManager, read_messages=True, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
        await channelOpgg.set_permissions(role, read_messages=True, send_messages=False, connect=True, speak=True, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
        channelAnnonce = await ctx.guild.create_text_channel(f"📌𝐀𝐧𝐧𝐨𝐧𝐜𝐞", category = category)
        await channelAnnonce.set_permissions(role, read_messages=True, send_messages=False, connect=True, speak=True, add_reactions = True, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
        channelAnalyse = await ctx.guild.create_text_channel(f"🔎𝐀𝐧𝐚𝐥𝐲𝐬𝐞", category = category)
        await channelAnalyse.set_permissions(role, read_messages=True, send_messages=False, connect=True, speak=True, add_reactions = True, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=True, stream=True, priority_speaker=False, send_tts_messages=False)
        channelChampionPool = await ctx.guild.create_text_channel(f"🏹𝐂𝐡𝐚𝐦𝐩𝐢𝐨𝐧-𝐏𝐨𝐨𝐥", category = category, sync_permissions=True)
        channelDraft = await ctx.guild.create_text_channel(f"📖𝐃𝐫𝐚𝐟𝐭", category = category, sync_permissions=True)
        channelAbscence = await ctx.guild.create_text_channel(f"🕞𝐀𝐛𝐬𝐞𝐧𝐜𝐞", category = category, sync_permissions=True)
        channelGeneral = await ctx.guild.create_text_channel(f"☕𝐆𝐞́𝐧𝐞́𝐫𝐚𝐥-{name_team}", category = category)
        voiceChannel = await ctx.guild.create_voice_channel(f"🎧𝐆𝐞́𝐧𝐞́𝐫𝐚𝐥", category = category)
        
        MysqlDef.addTeam(conn, team_id, serveur_id, name_team, category.id, channelOpgg.id, channelAnnonce.id, channelAnalyse.id, channelChampionPool.id,  channelDraft.id, channelAbscence.id, channelGeneral.id, voiceChannel.id, 0)

        await setTeamCreation(0)
        
        conn.close()

        await msgWait.delete()
        await ctx.channel.send(f"La team : **{name_team}** vient d'être créée.")


#------------------------------------------------#
#                   Add Joueur                   #
#------------------------------------------------#

@client.command(brief="")
async def addJoueur(ctx, person : discord.Member = None, pseudo = None, poste: int = 0, team_id : int = 0):
    
    if ctx.author.id in WHITELIST_IDS:
        if person is None : 
            await ctx.send("Vous n'avez pas renseigné le joueur.")
        else:
            if ctx.channel.id != 864909622061695006:
                await ctx.message.delete()

            serveur_id = ctx.guild.id

            conn = MysqlDef.connectionBDD()

            try:

                me = lol_watcher.summoner.by_name(my_region, f"{pseudo}")
                my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
            except ApiError  as error:
                if error.response.status_code == 400:
                    await ctx.send(f"({error.response.status_code}) Bad Request : Vérifier le nom d'invocateur. | {error}")
                elif error.response.status_code == 401:
                    await ctx.send(f"({error.response.status_code}) Unauthorized : La clé API n'est pas renseignée. | {error}")
                elif error.response.status_code == 403 :
                    await ctx.send(f"({error.response.status_code}) Forbidden : La clé API n'est pas valide. | {error}")
                elif error.response.status_code == 404  :
                    await ctx.send(f"({error.response.status_code}) Not found : Le serveur n'a pas trouvé de match pour la requête demandée. | {error}")
                elif error.response.status_code == 500  :
                    await ctx.send(f"({error.response.status_code}) ISE : Erreur interne au serveur de Riot. | {error}")
                elif error.response.status_code == 503 :
                    await ctx.send(f"({error.response.status_code}) SU : Les serveurs de Riot sont momentanément indisponibles. | {error}")
                else:
                    await ctx.send(f"({error.response.status_code}) Erreur Inconnue : Attendez un administrateur... | {error}")

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
            
            divTotal = 0

            guild = discord.utils.find(lambda g : g.id == ctx.guild.id, client.guilds)
            
            elo = 0
            div = 0
            divTotal = 0
            
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

            await removeAllRoleElo(person, guild)
            await person.add_roles(role)

            MysqlDef.addUser(conn, person.id, serveur_id, me['id'], pseudo, poste, divTotal, team_id, 1)

            TeamNewInfo = MysqlDef.getTeamForUser(conn, person.id)

            for Team in TeamNewInfo:
                newIdTeam = Team[0]
                newNameTeam = Team[1]

            newTeamRole = discord.utils.get(ctx.guild.roles, name = f'{newNameTeam}')

            await person.add_roles(newTeamRole)

            await updateOPGGTeam(ctx.guild, newIdTeam)
            await updateTeamElo(newIdTeam)

            conn.close()

            await ctx.send(f"Le joueur **{person.name}** a été ajouté à la team **{newNameTeam}**.")
    else:
        await ctx.send("Vous n'avez pas les droits pour exécuter cette commande.")

#------------------------------------------------#
#                                                #
#                   DELETE USER                  #
#                                                #
#------------------------------------------------#

@client.command(brief="")
async def deleteUser(ctx, person : discord.Member = None):
    if ctx.author.id in WHITELIST_IDS:
        if person is None:
            await ctx.send("Vous devez renseigner un nom de joueur. | Ex : !deleteUser \"<pseudoDiscord>\"")
        else:
            conn = MysqlDef.connectionBDD()

            TeamInfo = MysqlDef.getTeamForUser(conn, person.id)

            oldIdTeam = 0
            oldNameTeam = ""
            for Team in TeamInfo:
                oldIdTeam = Team[0]
                oldNameTeam = Team[1]

            MysqlDef.delUser(conn, person.id)

            await checkTeamEmpty(oldIdTeam)
            check = MysqlDef.checkIfTeamEmpty(conn, oldIdTeam)
            for c in check:
                if c[0] != 0:
                    await updateOPGGTeam(ctx.guild, oldIdTeam)
                    await updateTeamElo(oldIdTeam)
            await deleteEmptyTeam(oldIdTeam)

            oldTeam = discord.utils.get(ctx.guild.roles, name = f'{oldNameTeam}')

            await person.remove_roles(oldTeam)

            conn.close()

            await ctx.send(f"Le joueur **{person.name}** a été retiré de la team **{oldNameTeam}**")
    else:
        await ctx.send("Vous n'avez pas les droits pour exécuter cette commande.")

#------------------------------------------------#
#                                                #
#                Change Team Name                #
#                                                #
#------------------------------------------------#

@client.command(brief="")
async def teamName(ctx, id = None, name = None):
    if ctx.author.id in WHITELIST_IDS:
        if name is None:
            await ctx.send("Vous devez renseigner un nom de team. | Ex : !teamName <id_team> \"<name>\"")
        else:
            if id is None :
                await ctx.send("Vous devez renseigner l'ID de la team. | Ex : !teamName <id_team> \"<name>\"")
            else:
                conn = MysqlDef.connectionBDD()
                serveur_id = ctx.guild.id

                teamInfo = MysqlDef.getTeamName(conn, id, serveur_id)

                for t in teamInfo:
                    oldTeamName = t[0]
                    categorie = client.get_channel(t[1])
                    general = client.get_channel(t[2])

                role = discord.utils.get(ctx.guild.roles, name=f"{oldTeamName}")

                await role.edit(name = f"{name}")

                await categorie.edit(name=f"{name}")

                tag = name[0:3]

                await general.edit(name=f"☕𝐆𝐞́𝐧𝐞́𝐫𝐚𝐥-{tag}")

                MysqlDef.changeTeamName(conn, id, name)

                conn.close()

                await ctx.send(f"La team **{oldTeamName}** s'appelle maintenant **{name}**")
    else:
        await ctx.send("Vous n'avez pas les droits pour exécuter cette commande.")

#----------------------------------------------------#
#                   Reset Mentorat                   #
#----------------------------------------------------#

@client.command(brief="")
async def resetMentorat(ctx):
    conn = MysqlDef.connectionBDD()
    server_id = ctx.guild.id
    MysqlDef.setMentorat(conn, server_id, 0, 0, 0, 0)
    conn.close()


@client.command()
async def getRiotId(ctx, person = None):

    now = datetime.datetime.now()

    try:
        me = lol_watcher.summoner.by_name(my_region, f"{person}")
        await ctx.channel.send(me['id'])
    except ApiError as error:
        await Message.errorApi(ctx.channel, now, error)
        return



















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
        data[serveur_id]["mentor"] = {}
        data[serveur_id]["student"] = {}
        
        with open('/home/Production/Qualia/server.json','w') as f:
            json.dump(data, f, indent=4)
            f.close()
        
        conn.close()


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
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Réagissez à ce message par cette réaction pour commencer votre inscription.", value="📝")
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction("📝")

        MysqlDef.setMessageReaction(conn, serveur_id, msg.id)

        conn.close()


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
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
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

        conn.close()


#-------------------------------------------------------------#
#           Initialise le message des rôles lol               #
#-------------------------------------------------------------#

@client.command()
async def initMessageRoleJeux(ctx):
    if ctx.author.id not in WHITELIST_IDS:
        await ctx.channel.send("Vous n'avez pas la permission d'utiliser cette commande.")
    else:
        conn = MysqlDef.connectionBDD()
        serveur_id = ctx.guild.id

        await ctx.message.delete()

        embed=discord.Embed(title="Choisissez vos jeux favoris !", color = discord.Color(0xFDFF00))
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Les différents jeux :", value="> <:LeagueofLegends:867442026060185640> League of Legends \n > <:Valorant:867429253506269205> Valorant \n > <:TFT:867438874975010826> TFT \n > <:CSGO:867439458982690856> CS:GO \n > <:RocketLeague:867439656198864907> Rocket League \n > <:Hearthstone:867431647459672074> HearthStone \n > <:Chess:867439802651901983> Chess \n", inline=False)
        msg = await ctx.channel.send(embed = embed)
        await msg.add_reaction("<:LeagueofLegends:867442026060185640>")
        await msg.add_reaction("<:Valorant:867429253506269205>")
        await msg.add_reaction("<:TFT:867438874975010826>")
        await msg.add_reaction("<:CSGO:867439458982690856>")
        await msg.add_reaction("<:RocketLeague:867439656198864907>")
        await msg.add_reaction("<:Hearthstone:867431647459672074>")
        await msg.add_reaction("<:Chess:867439802651901983>")

        MysqlDef.setMessageRoleJeu(conn, serveur_id, msg.id)

        conn.close()

#--------------------------------------------------------------------#
#           Initialise la catégorie pour le Mendatorat               #
#--------------------------------------------------------------------#

@client.command()
async def initMentorat(ctx):
    conn = MysqlDef.connectionBDD()
    server_id = ctx.guild.id
    
    check = MysqlDef.getMentorat(conn, server_id)

    for c in check:
        if c[0] != 0:
            await ctx.channel.send("Votre serveur possède déjà ces salons de Mentorat. Si vous les avez supprimés, veuillez taper la commande suivante : **!resetMentorat**")
            return

    #------------------------------------------------#
    #                     Category                   #
    #------------------------------------------------#
    category = await ctx.guild.create_category("Mentorat", overwrites=None, reason=None)

    roleMentor = discord.utils.get(ctx.guild.roles, name="mentor")
    roleEleve = discord.utils.get(ctx.guild.roles, name="élève")

    await category.set_permissions(ctx.guild.default_role, read_messages=True, send_messages=False, connect=True, speak=True, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=True, priority_speaker=False, send_tts_messages=False)

    #------------------------------------------------#
    #                    Channel                     #
    #------------------------------------------------#

    channel = await ctx.guild.create_text_channel('📝 Seek-mentoring', category=category)
    channelMentor = await ctx.guild.create_text_channel('📘 Seek-mentor', category=category)
    await channelMentor.set_permissions(roleEleve, read_messages=True, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
    await channelMentor.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
    channelMentee = await ctx.guild.create_text_channel('📚 Seek-élève', category=category)
    await channelMentee.set_permissions(roleMentor, read_messages=True, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
    await channelMentee.set_permissions(ctx.guild.default_role, read_messages=False, send_messages=False, connect=False, speak=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, use_voice_activation=False, stream=False, priority_speaker=False, send_tts_messages=False)
    

    embed=discord.Embed(title="Bienvenue sur le système de Mentorat du serveur", color = discord.Color(0xFDFF00))
    embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
    embed.add_field(name="Ce système de mentorat va vous permettre de vous entraider au sein du serveur.", value="Plusieurs choix s'offrent à vous :", inline=False)
    embed.add_field(name="👨🏽‍🏫 Devenir MENTOR :", value=" > Être respectueux.\n > Vouloir enseigner.\n > Avoir un certains nombre de connaissances.", inline=False)
    embed.add_field(name="📚 Être MENTORÉ :", value=" > Être respectueux.\n > Vouloir apprendre.", inline=False)
    embed.set_footer(text = f"Si l'aventure vous tente, réagissez au message pour commencer la procédure !")
    msg = await channel.send(embed = embed)

    await msg.add_reaction("👨🏽‍🏫")
    await msg.add_reaction("📚")

    MysqlDef.setMentorat(conn, server_id, msg.id, channelMentor.id, channelMentee.id, category.id)


    conn.close()
























#------------------------------------------------#
#                                                #
#               Fonctions Glbales                #
#                                                #
#------------------------------------------------#

#------------------------------------------------#
#               Check Team Empty                 #
#------------------------------------------------#
async def checkTeamEmpty(team_id):
    conn = MysqlDef.connectionBDD()

    count = MysqlDef.checkIfTeamEmpty(conn, team_id)

    for c in count:
        if c[0] == 0:
            await channelPurge(team_id)

    conn.close()

#------------------------------------------------#
#              Delete Empty Team                 #
#------------------------------------------------#
async def deleteEmptyTeam(team_id):
    conn = MysqlDef.connectionBDD()

    count = MysqlDef.checkIfTeamEmpty(conn, team_id)

    for c in count:
        if c[0] == 0:
            await channelDelete(team_id)

    conn.close()

#------------------------------------------------#
#               Purge Team Empty                 #
#------------------------------------------------#
async def channelPurge(team_id):
    conn = MysqlDef.connectionBDD()

    channels = MysqlDef.getChannelOfTeamById(conn, team_id)

    channel = None
    for channel in channels[0]:
        if channel != 0:
            chan = client.get_channel(channel)
            await chan.purge()
 
    conn.close()

#------------------------------------------------#
#              Delete Team Empty                 #
#------------------------------------------------#
async def channelDelete(team_id):
    conn = MysqlDef.connectionBDD()

    channels = MysqlDef.getAllChannelOfTeamById(conn, team_id)
    print(f"-------------------------------------- GET CHANNEL AND DELETE for team : {team_id} ")

    channel = None
    print(channels)
    for channel in channels[0]:
        if channel != 0:
            chan = client.get_channel(channel)
            await chan.delete()

    MysqlDef.deleteTeam(conn, team_id)

    conn.close()

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
        poste_name = "JUNGLE"
    elif int(poste) == 2:
        poste_name = "MID"
    elif int(poste) == 3:
        poste_name = "ADC"
    elif int(poste) == 4:
        poste_name = "SUPPORT"
    
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
#               Add player to team               #
#------------------------------------------------#

async def addPlayerToTeam(conn, user1, user2, user3, user4, user5, serveur_id, riot_id, name, userElo, team_id, compteur):
    if compteur == 0:
        MysqlDef.addUser(conn, user1.id, serveur_id, riot_id, name, 0, userElo, team_id, 1)
    elif compteur == 1:
        MysqlDef.addUser(conn, user2.id, serveur_id, riot_id, name, 1, userElo, team_id, 1)
    elif compteur == 2:
        MysqlDef.addUser(conn, user3.id, serveur_id, riot_id, name, 2, userElo, team_id, 1)
    elif compteur == 3:
        MysqlDef.addUser(conn, user4.id, serveur_id, riot_id, name, 3, userElo, team_id, 1)
    elif compteur == 4:
        MysqlDef.addUser(conn, user5.id, serveur_id, riot_id, name, 4, userElo, team_id, 1)

#------------------------------------------------#
#                update OPGG Team                #
#------------------------------------------------#

async def updateOPGGTeam(guild, team_id):

    conn = MysqlDef.connectionBDD()

    channels = MysqlDef.getChannelAAAByTeamId(conn, team_id)

    channelAAA = None
    for channel in channels[0]:
        channelAAA = client.get_channel(channel)
        await channelAAA.purge()

    check = MysqlDef.checkUsersInTeamByTeamID(conn, team_id)
    for c in check :
        if c[0] != 0:
            description = await getTeamDescription(team_id) 
            embed=discord.Embed(title="Information sur les joueurs de la team :")
            embed.set_author(name="Qualia" , icon_url="https://zupimages.net/up/21/28/xrxs.png")

            if 'TOP' in description.keys():
                idTop = int(description["TOP"]["discordTag"])
                tagTop = guild.get_member(idTop)
                nameTop = description["TOP"]["discordName"]
                embed.add_field(name = f"TOP", value = f"{tagTop} ({nameTop})", inline=False)

            if 'JUNGLE' in description.keys():
                idJgl = int(description["JUNGLE"]["discordTag"])
                tagJgl = guild.get_member(idJgl)
                nameJgl = description["JUNGLE"]["discordName"]
                embed.add_field(name = f"JUNGLE", value = f"{tagJgl} ({nameJgl})", inline=False)

            if 'MID' in description.keys():
                idMid = int(description["MID"]["discordTag"])
                tagMid = guild.get_member(idMid)
                nameMid = description["MID"]["discordName"]
                embed.add_field(name = f"MID", value = f"{tagMid} ({nameMid})", inline=False)
            
            if 'ADC' in description.keys():
                idAdc = int(description["ADC"]["discordTag"])
                tagAdc = guild.get_member(idAdc)
                nameAdc = description["ADC"]["discordName"]
                embed.add_field(name = f"ADC", value = f"{tagAdc} ({nameAdc})", inline=False)

            if 'SUPPORT' in description.keys():
                idSupp = int(description["SUPPORT"]["discordTag"])
                tagSupp = guild.get_member(idSupp)
                nameSupp = description["SUPPORT"]["discordName"]
                embed.add_field(name = f"SUPPORT", value = f"{tagSupp} ({nameSupp})", inline=False)

            await channelAAA.send(embed = embed)

            httpLink = await getTeamOPGG(team_id)

            await channelAAA.send(httpLink)

    conn.close()
    
#------------------------------------------------#
#              Get Team Discription              #
#------------------------------------------------#
async def getTeamDescription(team_id):
    conn = MysqlDef.connectionBDD()

    users = MysqlDef.getUsersInTeamByTeamID(conn, team_id)

    description = {}
    for user in users:
        userPoste = await getPosteName(user[1])
        description[userPoste] = {"discordTag" : user[2], "discordName" : user[0]}

    conn.close()

    return description

#------------------------------------------------#
#                 Get Team OP GG                 #
#------------------------------------------------#
async def getTeamOPGG(team_id):
    conn = MysqlDef.connectionBDD()

    users = MysqlDef.getUsersInTeamByTeamID(conn, team_id)

    httpLink = "https://euw.op.gg/multi/query="
    compteur = 0
    for user in users:
        userPseudo = user[0]
        userPseudo = userPseudo.replace(" ", "%20")
        if compteur == 0:
            httpLink = httpLink + userPseudo
            compteur += 1
        else:
            httpLink = httpLink + "%2C" + userPseudo

    conn.close()

    return httpLink


#------------------------------------------------#
#                Update Elo Team                 #
#------------------------------------------------#
async def updateTeamElo(team_id):
    conn = MysqlDef.connectionBDD() 

    countNumber = MysqlDef.checkUsersInTeamByTeamID(conn, team_id)   # On compte le nombre de joueur présent dans la team
    for cn in countNumber:
        number = cn[0]

    users = MysqlDef.getUsersEloInTeamByTeamID(conn, team_id) # On récupère l'elo des joueurs de l'équipe

    divList = 0
    for user in users:
        divList += user[0]

    divMoy = 0

    if number != 0:
        divMoy = divList/number
        if divMoy%1 <= 0.5:
            divMoy = floor(divMoy) # On fait la moyenne des joueurs arrondi négatif
        else:
            divMoy = ceil(divMoy) # On fait la moyenne des joueurs arrondi positif

    MysqlDef.updateTeamEloMoy(conn, divMoy, team_id)

    conn.close()


#------------------------------------------#
#                Get Débat                 #
#------------------------------------------#
async def getInfo(nbr):
    rst = ""

    if nbr == 0:
        rst = "entendre"
    elif nbr == 1:
        rst = "voir"

    return rst


















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

@aiocron.crontab('0/15 * * * *')
async def checkAPI():
    listOfUser = ["kODUCOn3DpajEAJnW2_LMHLKXL6-JjkIcdWzisROLwzKgDs", "VU3uNSqZWD2AWnzIDFNQtsol-SIt5_V7nkSo6htR8aXl2RA", "zSCn3iycR432lx_7hvE41alcd3ZMtPcteYvSWduK7tJRChI", "zFrR26hxnkPvn1DEomMx14I_V6yXk1TZmVjjd0dIZ6OBrB0", ] # 
    riotUserId = random.choice(listOfUser)
    channelAdmin = client.get_channel(864909655259217940)
    now = datetime.datetime.now()
    print(f" CHECK API : {now}")

    try:
        my_ranked_stats = lol_watcher.league.by_summoner(my_region, riotUserId)
    except ApiError as error:
        await Message.errorApi(channelAdmin, now, error)
        return

#---------------------------------------------------#
#           Update User with Riot API               #
#---------------------------------------------------#
"""
Cette fonction vérifie si l'elo de chaque joueur à changé
depuis la nuit dernière. Si tel est le cas, la fonction
remet à jour les informations du joueur et de la team.
@aiocron.crontab('0 2 * * *')
async def updateRiotAPI():
    conn = MysqlDef.connectionBDD()
    #serv_id = ctx.guild.id
    users = MysqlDef.getAllUser(conn, serv_id) # id_riot, discord_id, name, div, team
    guild = client.get_guild(627766433761198103)
    channel = client.get_channel(841379535030321152)
    now = datetime.datetime.now()
    await channel.send("------------------------------------------")
    await channel.send(f" UPDATE USER (RIOT API) : {now}")
    for user in users:
        try:
        
            my_ranked_stats = lol_watcher.league.by_summoner(my_region, user[0])
            for i in range(len(my_ranked_stats)) : 
                if my_ranked_stats[i]['queueType'] == "RANKED_SOLO_5x5":
                    #-----------------------------------#
                    #             Variables             #
                    #-----------------------------------#
                    elo = await getElo(my_ranked_stats[i]['tier'])
                    div = await getEloDiv(my_ranked_stats[i]['rank'])
                    divTotal = await calculUserElo(int(elo), int(div))
                    #-----------------------------------#
                    #            Name check             #
                    #-----------------------------------#
                    if user[2] != my_ranked_stats[i]['summonerName']:
                        MysqlDef.changeUserPseudo(conn, my_ranked_stats[0]['summonerName'], user[1])
                        await updateOPGG(user[4], guild)
                        await channel.send(f"Old Summoner Name : {user[2]} | New Summoner Name : {my_ranked_stats[i]['summonerName']}")
                    #-----------------------------------#
                    #           Division check          #
                    #-----------------------------------#
                    if user[3] != int(divTotal):
                        print(divTotal)
                        MysqlDef.changeUserElo(conn, user[1], divTotal)
                        await updateTeamElo(user[4])
                        oldCalculElo, oldCalculDiv = await calculInvUserElo(user[3])
                        oCalculElo = await getEloName(oldCalculElo)
                        oCalculDiv = await getDivName(oldCalculDiv)
                        await channel.send(f"{my_ranked_stats[i]['summonerName']} | {oCalculElo} {oCalculDiv} --> {my_ranked_stats[i]['tier']} {my_ranked_stats[i]['rank']}")  
                        role_iron = discord.utils.get(guild.roles, name = 'Iron (Lol)')
                        role_bronze = discord.utils.get(guild.roles, name = 'Bronze (Lol)')
                        role_silver = discord.utils.get(guild.roles, name = 'Silver (Lol)')
                        role_gold = discord.utils.get(guild.roles, name = 'Gold (Lol)')
                        role_plat = discord.utils.get(guild.roles, name = 'Platinum (Lol)')
                        role_diam = discord.utils.get(guild.roles, name = 'Diamond (Lol)')
                        member = guild.get_member(user[1])
                        upperCaseElo = my_ranked_stats[i]['tier'].upper()
                        newElo = await getElo(upperCaseElo)
                        if oCalculElo != newElo:
                            #------------------------------------------------#
                            #                  Remove Role                   #
                            #------------------------------------------------#
                            if role_iron in member.roles:
                                await member.remove_roles(role_iron)
                            if role_bronze in member.roles:
                                await member.remove_roles(role_bronze)
                            if role_silver in member.roles:
                                await member.remove_roles(role_silver)
                            if role_gold in member.roles:
                                await member.remove_roles(role_gold)
                            if role_plat in member.roles:
                                await member.remove_roles(role_plat)
                            if role_diam in member.roles:
                                await member.remove_roles(role_diam)
                            #------------------------------------------------#
                            #                    Add Role                    #
                            #------------------------------------------------#
                            if newElo == 0:
                                await member.add_roles(role_iron)
                            elif newElo == 1:
                                await member.add_roles(role_bronze)
                            elif newElo == 2:
                                await member.add_roles(role_silver)
                            elif newElo == 3:
                                await member.add_roles(role_gold)
                            elif newElo == 4:
                                await member.add_roles(role_plat)
                            elif newElo == 5:
                                await member.add_roles(role_diam)
                        
            
        except ApiError as error:
            await channel.send(f"{user} div : {divTotal} | La clé d'API Riot n'est plus valide. | {error}")
            return
        except Exception as error:
            await channel.send(f"{user} div : {divTotal} | Une erreur est survenue : {error}")
            return
            
    now = datetime.datetime.now()
    await channel.send(f" UPDATE USER END : {now}")
    await channel.send("------------------------------------------")
    conn.close()
"""
client.run(TOKEN)