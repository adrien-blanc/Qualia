# READ_ME - Qualia
## Description
Ce projet a été crée dans l'objectif de fournir un BOT [Discord](https://discord.com/) sur le serveur communautaire d'un ami.
Il permet entre autres de :
* provisionner automatiquement tous les channels nécessaires au fonctionnement d'une équipe dans la structure.
* d'ajouter des joueurs à ces équipes.
* fournir des salons vocaux qui se créent et se suppriment automatiquement lorsqu'il n'y a plus personne dedans.
* fournir un système de mentor/élève pour que la communauté s'entraide.
* créer un message pour ajouter les rôles automatiquement en fonction des réactions des gens.

**Disclamer** :  Ce bot a été pensé pour fonctionner sur un serveur en particulier. Autrement dit, vous devrez surement vérifier l'intégralité du code afin de vous assurer que des IDs ne seraient pas en dur dans le code. Je ne pense pas qu'en tant que tel vous puissiez faire grand chose avec ces lignes de codes, car ça n'a tout simplement pas été pensé pour être rendu publique. En revanche, je reste intimement convaincu que plusieurs méthodes et subtilités de l'API de Discord vous seront utiles, tant j'ai eu du mal à les trouver à mes débuts.
## Prerequisites
- Serveur Linux (machine virtuel par exemple)
- Python3
- MySQL Server


## How to deploy
Tout d'abord, il vous faut un serveur pour héberger votre BOT. Vous n'avez pas besoin d'avoir une machine très puissante, la plupart des machines virtuelles que l'on trouve à 3-4€/mois dans le Cloud font l'affaire.
Une fois sur votre machine je vous conseil de déployer votre BOT sous la forme d'un service. Voici un rapide tutoriel :
En ligne de commande linux, cloner le repository :
 ```bash
git clone git@github.com:adrien-blanc/Qualia.git
cd Qualia

python3 -m venv venv
source venv/bin/activate

pip3 install -r requirements.txt

# Facultatif (permet de mettre à jour les paquages):
pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U && pip3 freeze > requirements.txt

export $PATH=<path_to_your_repository> > ~/.bash_profile
source ~/.bash_profile

cd /etc/systemd/system
nano <service_name>.service
```
Insérer ensuite dans le fichier créé ceci :
```service
[Unit]
Description=Discord bot
After=network.target

[Service]
Type=simple
Restart=on-failure
EnvironmentFile=$PATH/vars.py
ExecStart=$PATH/venv/bin/python3 $PATH/main.py

[Install]
WantedBy=multi-user.target
```

Puis on va lancer le service :
```bash
systemctl daemon-reload
systemctl enable <service_name>.service
systemctl start <service_name>.service
```

Comme vous avez peut-être pu le voir dans le fichier <service_name>.service créé précédemment, il va falloir créer un fichier vars.py contenant nos variables d'environnement (ne pas les publier sur internet) :
```python
TOKEN = '***' # <- Token à récupérer sur le site officiel de Discord Développeur 
RIOT_API_KEY = '***' # <- Token à récupérer sur le site officiel de RIOT Games Développeur 
HOSTNAME = "127.0.0.1" # <- Ici se trouve l'adresse IP de votre base de données MySQL,
# mais pour plus de sécurité je vous conseille de bloquer l'accès à l'extérieur et de vous
# servir de l'adresse de LocalHost de votre machine hôte.

USERNAME = "<database_login_name>"
PASSWORD = "<database_password>"
DATABASE = "<database_name>"
WHITELIST_IDS = [111111111111111111, 22222222222222222, 3333333333333333333] # Permet de choisir qui pourra exécuter les commandes.
BLACKLIST_IDS = [444444444444444444]
LOGS_ID = <ID_Channel_for_Log>
VERSION = "1.0.2" # <- Facultatif : Permet de versionner les différentes étapes d'avancement de votre BOT.
```

## Voici les commandes que vous pourrez utiliser avec ce BOT :
**!createTeam** : Créer une nouvelle équipe. 
**!addJoueur <discord_pseudo> <pseudo_en_jeu> <poste> <id_team>** : Ajoute un joueur à une équipe. Le poste doit être renseigné selon la liste suivante :

> TOP : 0 
> JUNGLE : 1 
> MID : 2 
> ADC : 3 
> SUPPORT : 4

**!purge** : Permet de supprimer l'intégralité des messages d'un channel. 
**!deleteMentor** <discord_pseudo> : Supprime un mentor de la BDD et lui enlève le rôle. 
**!deleteStudent** <discord_pseudo> : Supprime un élève de la BDD et lui enlève le rôle. 
**!initVoiceChannel** : Initlialise les channels vocaux automatiques. (Ne peut être fait qu'une fois par serveur) **!initMessage** : Initie dans le channel le message permettant l'inscription des joueurs. 
**!initMessageRole** : Initie dans le channel le message permettant de choisir son rôle et son élo.  
**!initMentorat** : Initie la catégorie de mentorat. (Ne peut être fait qu'une fois par serveur) **!initMessageRoleJeu** : Initie dans le channel le message permettant le choix des jeux.
**!updateOPGG** : Permet de mettre à jour les salons "opgg" de toutes les équipes si besoin.

## Rendu
Voici ce que la commande **!createTeam** fera :
Elle va créer une nouvelle catégorie avec le nom de l'équipe, elle va créer par la suite tous les salons que l'on a jugé nécessaire pour le bon fonctionnement de cette dernière. Elle va également créer un rôle spécifique à cette équipe et seul eux auront des droits spécifiques sur ces channels, comme les voir, écrire dedans, etc...
Salons :
![alt text](https://zupimages.net/up/22/24/yju2.png)

Rôle :
![alt text](https://zupimages.net/up/22/24/35ht.png)

La commande **!initVoiceChannel** va initialiser 4 Channels vocaux automatique. C'est-à-dire que lorsque que quelqu'un cliquera sur le salon *Flex* par exemple, un nouveau salon *Flex* sera crée et il sera déplacé dedans. Lorsque tout le monde aura quitté le serveur, le salon sera supprimé. Cela permet de générer un nombre infini de salon vocaux sans bloquer d'éventuelle personne qui n'aurait plus de salon libre, ou sans créer 120 salon vocaux comme on peut le voir sur certains serveurs ...
![alt text](https://zupimages.net/up/22/24/zr77.png)

Le noms de salon peut être changé dans le fichier ***server.json***, mais ce n'est pas vraiment fait pour, libre à vous de vous adapter comme vous le souhaitez. 
Pour le coup cette partie est faite pour fonctionner sur plusieurs serveurs simultanément. En revanche, le fait d'utiliser un fichier **Json** comme stockage des données n'est pas conseillé, des risques de perte de données peuvent avoir lieux si des demandes sont effectuées simultanément.

Dans un autre projet, je stock mes données dans une base de données **Cosmo DB** afin d'éviter à tout jamais ce genre de problème. Malheureusement le projet qui l'implémente est projet sur lequel je travail depuis plus d'un an et je ne peux me permettre de vous en montrer le code source. Je vous met tout de même un petit échantillon de ce à quoi ça pourrait ressembler :  

Voici un exemple de **ticketing**
Côté BDD, voici ma méthode de connexion :
```python
async  def  connectionMongoDBB(logs_channel): # le paramètre n'est pas nécessaire, il me permet de remonter mes erreurs sur un salon discord précis.
  try:
    conn = MongoClient("mongodb://localhost:27017/")
    return  conn
  except  Exception  as  error:
    await  logs_channel.send(error)
  return  0
```

Ensuite côté main.py ou methodes.py j'insert des données de cette manière :
```Python
async  def  connectToTicketDB(logs_channel):
  """
  It connects to the database and returns the collection
  :param logs_channel: The channel where the bot will send the error messages
  :return: The database collection is being returned.
  """
  try:
    conn = await  MysqlDef.connectionMongoDBB(logs_channel)
    db = conn['DB_name']
    return  db['tickets']
  except  Exception  as  error:
    await  logs_channel.send(error)
```

Puis j'appelle cette méthode pour récupérer ma database et pouvoir insérer des données :
```Python
async  def  ticketFunction(payload, guild, category, logs_channel):
  try:
    server_id = payload.guild_id # Je récupère l'ID de mon serveur Discord
    collection = await  Methodes.connectToTicketDB(logs_channel) # Je récupère la collection de ma BDD CosmoDB (méthode vu plus haut).
    projection = {"_id": server_id} # J'indique la projection sur laquelle je veux insérer mes datas, en l'occurence l'ID de mon serveur.
    data = collection.find(projection) # Je récupère les données afin de récupérer l'ID du dernier ticket ouvert.
    
    last_ticket=1
    
    for  d  in  data:
      for  key  in  d['tickets'].keys():
        last_ticket = int(key)+1
    
    new_id_ticket = await  Methodes.getNextTicketId(last_ticket, logs_channel)

    if  new_id_ticket != 0:
      # Ici je vais vérifier si le rôle correspondant à ce ticket existe déjà ou non.
      if  not (discord.utils.get(guild.roles, name=f"Ticket-{new_id_ticket}")):
        # Ici il existe, donc je le récupère.
        role = await  guild.create_role(name=f"Ticket-{new_id_ticket}")
      else:
        # Ici il n'existe pas, donc je le créer.
        role = discord.utils.get(guild.roles, name=f"Ticket-{new_id_ticket}")
      roleScrims = discord.utils.get(guild.roles, id=903342038429335632)

      await  payload.member.add_roles(role)

	  # Je crée le nouveau salon écrit et j'affecte les bons rôles.
      channelTickets = await  guild.create_text_channel(f'📋𝐓𝐢𝐜𝐤𝐞𝐭𝐬-{new_id_ticket}', category=category)
      await  channelTickets.set_permissions(role, read_messages=True, send_messages=True, add_reactions = True, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = True, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = True, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, stream=True, send_tts_messages=False)
      await  channelTickets.set_permissions(roleScrims, read_messages=False, send_messages=False, add_reactions = False, attach_files = False, external_emojis = False, mention_everyone = False, read_message_history = False, manage_channels = False, manage_permissions = False, manage_webhooks = False, create_instant_invite = False, manage_messages = False, embed_links=False, use_slash_commands=False, mute_members=False, deafen_members=False, move_members=False, stream=False, send_tts_messages=False)
      
      # Ici je vais appeller une méthode que l'on va voir juste après pour insérer le nouveau ticket dans ma BDD.
      if await  Methodes.addToTicketDB(collection, server_id, last_ticket, channelTickets, logs_channel):
	      return  channelTickets, role, new_id_ticket
      else:
	      await logs_channel.send("Ticket Function Error : Error during inserting data...")
		  return  0
    else:
      await  logs_channel.send("Ticket Function Error : Probably Get Json data failled...")
      return  0
  except  Exception  as  error:
    await  logs_channel.send(error)
    return  0
```

Méthode addToTicketDB :
```python
async  def  addToTicketDB(collection, serveur_id, id, channel, logs_channel):
	"""
	It takes the collection, the server id, the ticket id, the channel and the logs channel as
	parameters and then it tries to update the collection with the new ticket id and if it fails it
	sends the error to the logs channel
	:param collection: The collection in which the data is stored
	:param serveur_id: The ID of the server
	:param id: the id of the ticket
	:param channel: The channel that the ticket is in
	:param logs_channel: The channel where the bot will send the logs
	:return: the result of the update_many function.
	"""
	try:
		collection.update_many({"_id": serveur_id},{'$set': {"tickets.{}".format(id): channel.id}})
		return  1
	except  Exception  as  error:
		await  logs_channel.send(error)
	return  0
```

Voilà j'espère que cette partie sur CosmoDB aidera des gens à rendre leur stockage de données plus sûr.
