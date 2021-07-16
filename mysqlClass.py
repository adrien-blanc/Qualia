#------------------------------------------------#
# Projet appartenant à Adrien BLANC              #
# Créé et développé par Adrien BLANC             #
# Contact : adrien.blanc74@outlook.fr            #
#------------------------------------------------#


import mysql.connector
import vars

#------------------------------------------------#
#                                                #
#                 BDD connection                 #
#                                                #
#------------------------------------------------#

class MysqlDef():

    #------------------------------------------------#
    #                Global variable                 #
    #------------------------------------------------#

    def connectionBDD():
        conn = mysql.connector.connect(user=vars.USERNAME, 
            password=vars.PASSWORD,
            host=vars.HOSTNAME,
            database=vars.DATABASE)
        return conn

    #------------------------------------------------#
    #               Serveur functions                #
    #------------------------------------------------#

    def setServerInfo(conn, serveur_id, categorie):
        sql = f"INSERT INTO `serveur`(`serveur_id`, `categorie`, `reactionMessage`, `reactionRole`) VALUES ({serveur_id}, {categorie}, 0, 0);"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def getServerInfo(conn, serveur_id):
        sql = f"SELECT * FROM `serveur` WHERE `serveur`.`serveur_id` = {serveur_id};"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def checkIfServerExist(conn, serveur_id):
        sql = f"SELECT * FROM `serveur` WHERE `serveur`.`serveur_id` = {serveur_id};"
        cursor = conn.cursor()
        cursor.execute(sql)
        cursor.fetchall()
        if cursor.rowcount == 0:
            return False
        else:
            return True



    #  Message Réaction pour l'inscription  #

    def setMessageReaction(conn, serveur_id, msgReaction_id):
        sql = f"UPDATE `serveur` SET `reactionMessage` = {msgReaction_id} WHERE `serveur_id` = {serveur_id};"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def getMessageReaction(conn, serveur_id):
        sql = f"SELECT `reactionMessage`, `reactionRole` FROM serveur WHERE `serveur_id` = {serveur_id};"
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()


    #  Message Réaction pour les rôles  #

    def setMessageRole(conn, serveur_id, msgReaction_id):
        sql = f"UPDATE `serveur` SET `reactionRole` = {msgReaction_id} WHERE `serveur_id` = {serveur_id};"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    #------------------------------------------------#
    #                 Team functions                 #
    #------------------------------------------------#

    def setTeamCrea(conn, bool):
        sql = f"UPDATE `teamcrea` SET `bool`={bool} WHERE id_crea = 1;"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def getTeamCrea(conn):
        sql = f"SELECT `bool` FROM `teamcrea` WHERE id_crea = 1;"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def getNextTeamId(conn):
        sql = f"SELECT id_team FROM team;"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def addTeam(conn, team_id, team_name, team_categorie, team_channelOpgg, team_channelAnnonce, team_channelAnalyse, team_channelChampionPool, team_channelDraft, team_channelAbscence, team_channelGeneral, voiceChannel, elo_moy):
        sql = f"INSERT INTO `team`(`id_team`, `name`, `categorie_id`, `channelOpgg_id`, `channelAnnonce_id`, `channelAnalyse_id`, `channelChampionPool_id`, `channelDraft_id`, `channelAbscence_id`, `channelGeneral_id`, `voiceChannel`, `elo_moy`, `coach_id`) VALUES ({team_id},'{team_name}', {team_categorie}, {team_channelOpgg},{team_channelAnnonce}, {team_channelAnalyse}, {team_channelChampionPool}, {team_channelDraft}, {team_channelAbscence}, {team_channelGeneral}, {voiceChannel}, {elo_moy}, 0)"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def deleteTeam(conn, team_id):
        sql = f"DELETE FROM `team` WHERE `id_team` = {team_id};"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def getTeamPlayers(conn, team_id, serv_id):
        sql = f"SELECT `discord_id`, `pseudo`, `poste`, `div` FROM `users` WHERE (`users`.`team` = {team_id} AND `users`.`server_id` = {serv_id}) ORDER BY `users`.`poste` ASC;"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    
    #------------------------------------------------#
    #                 User functions                 #
    #------------------------------------------------#

    def setInfoUser(conn, discord_id, server_id, riot_id, pseudo, poste, div, team, search):
        sql = f"INSERT INTO `users`(`discord_id`, `server_id`, `riot_id`, `pseudo`, `poste`, `div`, `team`, `search`) VALUES ({discord_id}, {server_id}, '{riot_id}', '{pseudo}', {poste}, {div}, {team},{search}) ON DUPLICATE KEY UPDATE `server_id`={server_id}, `riot_id`='{riot_id}' , `pseudo`='{pseudo}', `poste`={poste}, `div`={div}, `team`={team}, `search`={search};"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()

    def getInfoUser(conn, server_id, discord_id):
        sql = f"SELECT `discord_id`, `server_id`, `riot_id`, `pseudo`, `poste`, `div`, `team`, `search` FROM `users` WHERE `server_id` = {server_id} AND `discord_id` = {discord_id};"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        return cursor.fetchall()

    def addUser(conn, user_id, serv_id, riot_id, pseudo, user_role, user_div, user_team, search):
        sql = f"INSERT INTO `users`(`discord_id`, `server_id`, `riot_id`, `pseudo`, `poste`, `div`, `team`, `search`) VALUES ({user_id}, {serv_id}, '{riot_id}', '{pseudo}', {user_role}, {user_div}, {user_team}, {search}) ON DUPLICATE KEY UPDATE `server_id`={serv_id}, `riot_id`='{riot_id}' , `pseudo`='{pseudo}', `poste`={user_role}, `div`={user_div}, `team`={user_team}, `search`={search};;"
        print(sql)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
