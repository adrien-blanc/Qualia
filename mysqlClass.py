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
        sql = f"INSERT INTO `serveur`(`serveur_id`, `categorie`, `reactionMessage`) VALUES ({serveur_id}, {categorie}, 0);"
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
        print(sql)
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
