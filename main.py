import discord
from discord import ui, app_commands
from client import client
from utils.messages import *
import pyrebase
import json
import os

if os.environ['BOT_LOCAL'] == "YES HOME!":
    with open('local.json','r') as f:
        config = json.load(f)
else:
    with open('config.json','r') as f:
        config = json.load(f)

firebase = pyrebase.initialize_app(config['firebase'])
db = firebase.database()
aclient = client(db=db)
bot = aclient.bot

@app_commands.command(name="gag",description="gags someone")
async def gag(inter:discord.Interaction,mem:discord.Member):
    db.child('guilds').child(inter.guild.id).child(mem.id).update({'gag':{'t_lvl':'higt'}})
    msg = f"{mem.display_name} was gagged{(f' by {inter.user.display_name}') if inter.user.id!=mem.id else ''}"
    await intersend(inter,inter.user,aclient,msg)
    await inter.response.send_message(msg,ephemeral=True)

@app_commands.command(name="ungag",description="ungags someone")
async def ungag(inter:discord.Interaction,mem:discord.Member):
    db.child('guilds').child(inter.guild.id).child(mem.id).update({'gag':None})
    msg = f"{mem.display_name} was ungagged{(f' by {inter.user.display_name}') if inter.user.id!=mem.id else ''}"
    await intersend(inter,inter.user,aclient,msg)
    await inter.response.send_message(msg,ephemeral=True)

bot.add_command(gag)
bot.add_command(ungag)
aclient.run(token=config['bot']['token'])

