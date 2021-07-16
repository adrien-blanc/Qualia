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
from mysqlClass import MysqlDef
from time import sleep


class Message():


    #------------------------------------------#
    #              Message Inscr               #
    #------------------------------------------#

    async def confirmationInscription(member):
        embed=discord.Embed(title="Procédure d'inscription")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Vous venez de commencer une procédure d'inscription.", value="Nous allons vous poser quelques questions sur vos objectifs au sein de l'assossiation.", inline=False)
        embed.add_field(name="Voici une liste des informations qui vont vous être demandées :", value="> - Votre pseudo IG\n> - Votre rôle\n> - Votre objectif au sein de l'assossiation", inline=False)
        embed.set_footer(text = f"Continuer : ✅ | Annuler : ❌")
        msg = await member.send(embed = embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        return msg

    async def inscriptionPseudo(member):
        embed=discord.Embed(title="Procédure d'inscription (**1/3**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Quel est votre **pseudo** dans le jeu *League Of Legends*", value="Attention réponse senssible à la case !", inline=False)
        msg = await member.send(embed = embed)
        return msg

    async def confirmePseudo(member, pseudo, eloSolo = None, divSolo = None, eloFlex = None, divFlex = None):
        embed=discord.Embed(title="Procédure d'inscription (**1/3**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        if (eloSolo is None) and (eloFlex is not None) :
            embed.add_field(name="Vérifier ces informations :", value=f"> Pseudo : **{pseudo}**\n > Solo/Duo | **Unranked**\n > Flex | **{eloFlex} {divFlex}**", inline=False)
        elif (eloSolo is not None) and (eloFlex is None) :
            embed.add_field(name="Vérifier ces informations :", value=f"> Pseudo : **{pseudo}**\n > Solo/Duo | **{eloSolo} {divSolo}**\n > Flex | **Unranked**", inline=False)
        elif (eloSolo is not None) and (eloFlex is not None) :
            embed.add_field(name="Vérifier ces informations :", value=f"> Pseudo : **{pseudo}**\n > Solo/Duo | **{eloSolo} {divSolo}**\n > Flex | **{eloFlex} {divFlex}**", inline=False)
        else:
            embed.add_field(name="Vérifier ces informations :", value=f"> Pseudo : **{pseudo}**\n > Solo/Duo | **Unranked**\n > Flex | **Unranked**", inline=False)
        embed.set_footer(text = f"Continuer : ✅ | Annuler : ❌")
        msg = await member.send(embed = embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        return msg

    async def inscriptionPoste(member):
        embed=discord.Embed(title="Procédure d'inscription (**2/3**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png") 
        embed.add_field(name="Quel est votre main poste actuelle ?", value = "Vous pourrez le changer par la suite.", inline=False)
        embed.set_footer(text = f"Réagissez avec le bon émoji ci-dessous.")
        msg = await member.send(embed = embed)
        await msg.add_reaction("<:Top:864176960493584455>")
        await msg.add_reaction("<:Jungle:864176942169325579>")
        await msg.add_reaction("<:Mid:864176925719134229>")
        await msg.add_reaction("<:Adc:864176890692370472>")
        await msg.add_reaction("<:Supp:864176867497476107>")
        return msg
    
    async def inscriptionChoix(member):
        embed=discord.Embed(title="Procédure d'inscription (**3/3**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Vous le savez peut-être déjà mais notre assossiation propose un service de coaching et d'équipe.", value="Vous avez la possibilité de rejoindre une équipe gratuitement.\nSi vous ne souhaitez pas rejoindre une équipe, vous pouvez tout simplement rester en simple joueur.\n Vous pourrez tout de même bénéficier du système de Tutorat proposé par l'assossation.", inline=False)
        embed.set_footer(text = f"Rejoindre un équipe : 1️⃣ | Rester simple joueur : 2️⃣")
        msg = await member.send(embed = embed)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        return msg

    async def inscriptionFin(member):
        embed=discord.Embed(title="Procédure d'inscription **terminée**")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Nous vous remerçions d'avoir pris le temps de répondre à ce questionnaire d'inscription.", value="Vos informations ont bien été enregistrées.", inline=False)
        embed.set_footer(text = f"Pour supprimer ce message : ✅")
        msg = await member.send(embed = embed)
        await msg.add_reaction("✅")
        return msg

    #------------------------------------------#
    #              Message Error               #
    #------------------------------------------#

    async def errorPseudo(member):
        embed=discord.Embed(title="Procédure d'inscription : **ERREUR**")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Nous n'avons pas pu retrouver votre pseudo", value="Si vous estimez l'avoir renseigné correctement, veillez contacter un administrateur.", inline=False)
        embed.set_footer(text = f"Ce message va s'auto-détruire. (10 secondes)")
        msg = await member.send(embed = embed)
        return msg
    
    async def error(member):
        embed=discord.Embed(title="Procédure d'inscription : **ERREUR**")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Une erreur est survenue durant votre inscription.", value="Veuillez contacter un administrateur.", inline=False)
        embed.set_footer(text = f"Ce message va s'auto-détruire. (10 secondes)")
        msg = await member.send(embed = embed)
        return msg

    async def inscriptionTempo(member):
        embed=discord.Embed(title="Procédure d'inscription : (**2/3**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Veuillez patienter", value="Cette étape peut prendre un certain temps.", inline=False)
        msg = await member.send(embed = embed)
        return msg

    #------------------------------------------#
    #              Message Admin               #
    #------------------------------------------#

    async def adminRecap(channelAdmin, member_id, member_name, riot_id, pseudo, poste, elo, div, team):
        embed=discord.Embed(title="Nouvelle inscription !")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name=f"Un nouveau joueur s'est inscrit : **{member_id} | {member_name}**", value=f" > **Riot ID** : {riot_id} \n > **Pseudo In-Game** : {pseudo}\n > **Poste** : {poste}\n > **Rang** : {elo} {div}\n > **Choix team :** : {team}", inline=False)
        embed.set_footer(text = f"Team : 1 | Pas Team : 0")
        msg = await channelAdmin.send(embed = embed)
        return msg
    
    async def getPseudo(channel, user):
        embed=discord.Embed(title="Information sur le joueur")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Quel est le pseudo en jeu de : ", value=f"**{user}**", inline=False)
        msg = await channel.send(embed = embed)
        return msg

    
    #-----------------------------------------#
    #              Message User               #
    #-----------------------------------------#

    async def userRecap(channelSeekTeam, member_name, pseudo, poste, elo, div, team):
        embed=discord.Embed(title="Nouveau joueur")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        if team == 1:
            embed.add_field(name=f"Un nouveau joueur arrive parmi nous, c'est **{member_name}**", value=f"\n > **Pseudo** : {pseudo}\n > **Poste** : {poste}\n > **Rang** : {elo} {div}\n > Il a fait le choix de rejoindre une **équipe** !", inline=False)
        elif team == 0:
            embed.add_field(name=f"Un nouveau joueur arrive parmi nous, c'est **{member_name}**", value=f"\n > **Pseudo** : {pseudo}\n > **Poste** : {poste}\n > **Rang** : {elo} {div}\n > Souhaite faire des games **communautaires** !", inline=False)
        embed.set_footer(text = f"N'hésitez pas à le contacter !")
        msg = await channelSeekTeam.send(embed = embed)
        return msg