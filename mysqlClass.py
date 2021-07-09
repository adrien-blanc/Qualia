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
    #                 User functions                 #
    #------------------------------------------------#

    