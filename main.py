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

    conn.close()
    
    

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
                    
                    
                    msgConfirmation = await Message.confirmePseudo(payload.member, pseudo, eloSolo, divSolo, eloFlex, divFlex)

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
                    msgError = await Message.errorPseudo(payload.member)

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
                await msgTempo.delete()
                msgChoix = await Message.inscriptionChoix(payload.member)

                def checkEmoji(reaction, user):
                    emoji_list = ["1️⃣", "2️⃣"]
                    return payload.user_id == user.id and msgChoix.id == reaction.message.id and (str(reaction.emoji) in emoji_list)

                reaction, user = await client.wait_for("reaction_add", check = checkEmoji)

                try:
                    channelAdmin = client.get_channel(864909655259217940)
                    channelSeekTeam = client.get_channel(865472953152045096)
                    posteName = await getPosteName(poste)
                    eloName = await getEloName(elo)
                    divName = await getDivName(div)
                    if reaction.emoji == "1️⃣":
                        await Message.userRecap(channelSeekTeam,payload.member.name, pseudo, posteName, eloName, divName, 1)
                        await Message.adminRecap(channelAdmin, payload.member.id, payload.member.name, me['id'], pseudo, posteName, eloName, divName, 1)
                        MysqlDef.setInfoUser(conn, payload.member.id, serveur_id, me['id'], pseudo, poste, divTotal, 0, 1)
                    elif reaction.emoji == "2️⃣":
                        await Message.userRecap(channelSeekTeam,payload.member.name, pseudo, posteName, eloName, divName, 0)
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
        embed.set_author(name="Qualia E-Sport", icon_url="https://zupimages.net/up/21/28/xrxs.png")
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

        conn.close()

























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

            if 'JGL' in description.keys():
                idJgl = int(description["JGL"]["discordTag"])
                tagJgl = guild.get_member(idJgl)
                nameJgl = description["JGL"]["discordName"]
                embed.add_field(name = f"JGL", value = f"{tagJgl} ({nameJgl})", inline=False)

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

            if 'SUPP' in description.keys():
                idSupp = int(description["SUPP"]["discordTag"])
                tagSupp = guild.get_member(idSupp)
                nameSupp = description["SUPP"]["discordName"]
                embed.add_field(name = f"SUPP", value = f"{tagSupp} ({nameSupp})", inline=False)

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
    listOfUser = ["DJ Malz", "LL Electrix", "DMara"] # "AzykOs",
    user = random.choice(listOfUser)
    now = datetime.datetime.now()
    print(f" CHECK API : {now}")

    try:
        me = lol_watcher.summoner.by_name(my_region, f"{user}")
        my_ranked_stats = lol_watcher.league.by_summoner(my_region, me['id'])
    except ApiError as error:
        await user.send(f"La clé d'API Riot n'est pas accessible. | {error} | https://developer.riotgames.com/")      
        return


client.run(TOKEN)