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

    async def waitTeam(channel):
        embed=discord.Embed(title="Création de l'équipe")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Veuillez patienter, cette opération peut prendre un certain temps.", value=f"environ 10 secondes...", inline=False)
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

    #---------------------------------------------#
    #                                             #
    #              Message Mentorat               #
    #                                             #
    #---------------------------------------------#

    #------------------------------------#
    #               MENTOR               #
    #------------------------------------#

    async def mentorInit(member):
        embed=discord.Embed(title="Inscription Mentor")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Vous venez de commencer une procédure d'inscription pour devenir Mentor !", value=f"Nous allons vous poser quelques questions sur vos objectifs au sein de se système de mentorat.", inline=False)
        embed.add_field(name="Voici une liste des informations qui vont vous être demandées :", value="> - Votre pseudo IG\n> - Votre rôle\n> - Vos objectifs", inline=False)
        embed.set_footer(text = f"Continuer : ✅ | Annuler : ❌")
        msg = await member.send(embed = embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        return msg

    async def mentorPseudo(member):
        embed=discord.Embed(title="Inscription Mentor : (**1/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Quel est votre **pseudo** dans le jeu *League Of Legends*", value="Attention réponse senssible à la case !", inline=False)
        msg = await member.send(embed = embed)
        return msg

    async def confirmePseudoMentor(member, pseudo, eloSolo = None, divSolo = None, eloFlex = None, divFlex = None):
        embed=discord.Embed(title="Inscription Mentor : (**2/6**)")
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

    async def mentorPoste(member):
        embed=discord.Embed(title="Inscription Mentor : (**3/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png") 
        embed.add_field(name="Sur quelle lane pensez-vous pouvoir enseigner ?", value = "Vous pourrez le changer par la suite.", inline=False)
        embed.set_footer(text = f"Réagissez avec le bon émoji ci-dessous.")
        msg = await member.send(embed = embed)
        await msg.add_reaction("<:Top:864176960493584455>")
        await msg.add_reaction("<:Jungle:864176942169325579>")
        await msg.add_reaction("<:Mid:864176925719134229>")
        await msg.add_reaction("<:Adc:864176890692370472>")
        await msg.add_reaction("<:Supp:864176867497476107>")
        return msg

    async def mentorNombre(member):
        embed=discord.Embed(title="Inscription Mentor : (**4/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png") 
        embed.add_field(name="Sur une échelle de 1 à 9", value = "comment noteriez-vous votre savoir ?", inline=False)
        embed.set_footer(text = f"Réagissez avec le bon émoji ci-dessous.")
        msg = await member.send(embed = embed)
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        await msg.add_reaction("3️⃣")
        await msg.add_reaction("4️⃣")
        await msg.add_reaction("5️⃣")
        await msg.add_reaction("6️⃣")
        await msg.add_reaction("7️⃣")
        await msg.add_reaction("8️⃣")
        await msg.add_reaction("9️⃣")
        return msg

    async def mentorPeda(member):
        embed=discord.Embed(title="Inscription Mentor : (**5/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png") 
        embed.add_field(name="Pensez-vous être pédagogue ou non ?", value = "Plutôt oui : ✅ | Plutôt moyen : ➕ | Plutôt non : ❌", inline=False)
        embed.set_footer(text = f"Réagissez avec le bon émoji ci-dessous.")
        msg = await member.send(embed = embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("➕")
        await msg.add_reaction("❌")
        return msg

    async def mentorMicroMacro(member):
        embed=discord.Embed(title="Inscription Mentor : (**6/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png") 
        embed.add_field(name="Êtes-vous plutôt un joueur micro ou macro ?", value = "Micro : 0️⃣ | Macro : 1️⃣ | Les deux : 2️⃣", inline=False)
        embed.set_footer(text = f"Réagissez avec le bon émoji ci-dessous.")
        msg = await member.send(embed = embed)
        await msg.add_reaction("0️⃣")
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        return msg

    async def mentorFin(member):
        embed=discord.Embed(title="Inscription Mentor : (**Terminé**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Nous avons terminé votre inscription en tant que mentor.", value="Merci d'avoir effectué cette démarche. Nous vous recontacterons au plus vite.", inline=False)
        embed.set_footer(text = f"Pour supprimer ce message : ✅")
        msg = await member.send(embed = embed)
        await msg.add_reaction("✅")
        return msg

    async def newMentor(channel, member_name,  pseudo, elo, div, poste, nbr, style):
        if style == 0:
            styleName = "micro"
        elif style == 1:
            styleName = "macro"
        elif style == 2:
            styleName = "micro / macro"


        embed=discord.Embed(title=f"Nouveau mentor !")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name=f"Voici les informations à propos de {member_name} :", value=f"> Pseudo : **{pseudo}**\n > Rang : **{elo} {div}**\n > Main poste : **{poste}**\n > Il pourra vous enseigner la **{styleName}**", inline=False)
        pseudo = pseudo.replace(" ", "+")
        embed.add_field(name=f"Voici son OP.GG", value=f"> https://euw.op.gg/summoner/userName={pseudo}", inline=False)
        embed.set_footer(text = f"Pour demander à se faire mentoré par {member_name} : ✅")
        msg = await channel.send(embed = embed)
        await msg.add_reaction("✅")
        return msg

    async def studentInfo(mentor, member, pseudo, eloSolo, divSolo, eloFlex, divFlex, poste, debat, apprendre, style):
        if style == 0:
            styleName = "micro"
        elif style == 1:
            styleName = "macro"
        elif style == 2:
            styleName = "micro / macro"

        embed=discord.Embed(title=f"Un élève a besoin de vous !")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        if debat == 1:
            embed.add_field(name=f"Voici les informations à propos de {member.name} :", value=f"> Pseudo : **{pseudo}**\n > Rang Solo : **{eloSolo} {divSolo}**\n > Rang Flex : **{eloFlex} {divFlex}**\n > Main poste : **{poste}**\n > Il a besoin de débattre pour assimiler.\n > Il veut {apprendre} les choses pour apprendre.\n > Il veux apprendre la **{styleName}**", inline=False)
        elif debat == 0:
            embed.add_field(name=f"Voici les informations à propos de {member.name} :", value=f"> Pseudo : **{pseudo}**\n > Rang Solo : **{eloSolo} {divSolo}**\n > Rang Flex : **{eloFlex} {divFlex}**\n > Main poste : **{poste}**\n > Il veux {apprendre} les choses pour apprendre.\n > Il veux apprendre la **{styleName}**", inline=False)
        pseudo = pseudo.replace(" ", "+")
        embed.add_field(name=f"Voici son OP.GG", value=f"> https://euw.op.gg/summoner/userName={pseudo}", inline=False)
        embed.set_footer(text = f"Accepter : ✅ | Refuser : ❌")
        msg = await mentor.send(embed = embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        return msg

    #-------------------------------------#
    #               STUDENT               #
    #-------------------------------------#

    async def studentRefus(member):
        embed=discord.Embed(title="Nous sommes désolé")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Nous sommes désolé mais le mentor que vous avez demandé n'a pas accepté votre demande.", value="Vous pouvez toujours demander à un autre mentor de vous aider.", inline=False)
        await member.send(embed = embed)

    async def studentAccept(member):
        embed=discord.Embed(title="Bravo")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Le mentor que vous avez demandé a accepté votre demande !", value="Un channel vocal et un channel écrit a été crée pour vous deux.", inline=False)
        await member.send(embed = embed)

    async def studentInit(member):
        embed=discord.Embed(title="Inscription élève")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Vous venez de commencer une procédure d'inscription pour devenir élève !", value=f"Nous allons vous poser quelques questions sur vos objectifs au sein de se système de mentorat.", inline=False)
        embed.add_field(name="Voici une liste des informations qui vont vous être demandées :", value="> - Votre pseudo IG\n> - Votre rôle\n> - Vos objectifs", inline=False)
        embed.set_footer(text = f"Continuer : ✅ | Annuler : ❌")
        msg = await member.send(embed = embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        return msg

    async def studentPseudo(member):
        embed=discord.Embed(title="Inscription élève : (**1/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        embed.add_field(name="Quel est votre **pseudo** dans le jeu *League Of Legends*", value="Attention réponse senssible à la case !", inline=False)
        msg = await member.send(embed = embed)
        return msg

    async def confirmePseudostudent(member, pseudo, eloSolo = None, divSolo = None, eloFlex = None, divFlex = None):
        embed=discord.Embed(title="Inscription élève : (**2/6**)")
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

    async def studentPoste(member):
        embed=discord.Embed(title="Inscription élève : (**3/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png") 
        embed.add_field(name="Sur quelle lane voulez-vous être coaché ?", value = "Vous pourrez le changer par la suite.", inline=False)
        embed.set_footer(text = f"Réagissez avec le bon émoji ci-dessous.")
        msg = await member.send(embed = embed)
        await msg.add_reaction("<:Top:864176960493584455>")
        await msg.add_reaction("<:Jungle:864176942169325579>")
        await msg.add_reaction("<:Mid:864176925719134229>")
        await msg.add_reaction("<:Adc:864176890692370472>")
        await msg.add_reaction("<:Supp:864176867497476107>")
        return msg

    async def studentDebat(member):
        embed=discord.Embed(title="Inscription élève : (**4/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png") 
        embed.add_field(name="Avez-vous besoin de débattre pour assimiler une information ?", value = "Oui j'ai besoin de débattre : 0️⃣ | Non pas besoin : 1️⃣", inline=False)
        embed.set_footer(text = f"Réagissez avec le bon émoji ci-dessous.")
        msg = await member.send(embed = embed)
        await msg.add_reaction("0️⃣")
        await msg.add_reaction("1️⃣")
        return msg

    async def studentApprendre(member):
        embed=discord.Embed(title="Inscription élève : (**5/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png") 
        embed.add_field(name="Avez-vous plutôt besoin d'**entendre** ou de **voir** les informations afin de les retenir ?", value = "Entendre : 0️⃣ | Voir : 1️⃣", inline=False)
        embed.set_footer(text = f"Réagissez avec le bon émoji ci-dessous.")
        msg = await member.send(embed = embed)
        await msg.add_reaction("0️⃣")
        await msg.add_reaction("1️⃣")
        return msg

    async def studentStyle(member):
        embed=discord.Embed(title="Inscription élève : (**6/6**)")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png") 
        embed.add_field(name="Voulez-vous apprendre la micro, la macro ou les deux ?", value = "Micro : 0️⃣ | Macro : 1️⃣ | Les deux : 2️⃣", inline=False)
        embed.set_footer(text = f"Réagissez avec le bon émoji ci-dessous.")
        msg = await member.send(embed = embed)
        await msg.add_reaction("0️⃣")
        await msg.add_reaction("1️⃣")
        await msg.add_reaction("2️⃣")
        return msg

    async def newStudent(chan, member_name,  pseudo, eloName, divName, posteName, debat, apprendre, style):
        if style == 0:
            styleName = "micro"
        elif style == 1:
            styleName = "macro"
        elif style == 2:
            styleName = "micro / macro"


        embed=discord.Embed(title=f"Nouvel élève !")
        embed.set_author(name="Qualia", icon_url="https://zupimages.net/up/21/28/xrxs.png")
        if debat == 1:
            embed.add_field(name=f"Voici les informations à propos de {member_name} :", value=f"> Pseudo : **{pseudo}**\n > Rang : **{eloName} {divName}**\n > Main poste : **{posteName}**\n > Il a besoin de débattre pour assimiler.\n > Il veut {apprendre} les choses pour apprendre. \n > Il souhaite apprendre la **{styleName}**", inline=False)
        elif debat == 0:
            embed.add_field(name=f"Voici les informations à propos de {member_name} :", value=f"> Pseudo : **{pseudo}**\n > Rang : **{eloName} {divName}**\n > Main poste : **{posteName}**\n > Il veut {apprendre} les choses pour apprendre. \n > Il souhaite apprendre la **{styleName}**", inline=False)
        pseudo = pseudo.replace(" ", "+")
        embed.add_field(name=f"Voici son OP.GG", value=f"> https://euw.op.gg/summoner/userName={pseudo}", inline=False)
        embed.set_footer(text = f"Si vous souhaitez mentorer {member_name} : ✅")
        msg = await chan.send(embed = embed)
        await msg.add_reaction("✅")
        return msg