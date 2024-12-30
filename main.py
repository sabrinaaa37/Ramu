import discord
from discord import ui, app_commands
from client import client
from utils.messages import *
from ui.register import RegisterView
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

@app_commands.command(name="register", description="register yourself with the bot for more stuff!")
async def register(inter:discord.Interaction):
    await inter.response.send_message(view=RegisterView(user=inter.user, db=db))

@app_commands.command(name="profile", description="lookup someone's profile or yours")
async def profile(inter:discord.Interaction, mem:discord.Member=None):
    data = db.child('members').child(mem.id).child('profile').get().val()
    if not data:
        await inter.response.send_message("User not registered")
        return
    embed = discord.Embed(
            title = f"__• Profile of {mem.display_name}__",
            color=discord.Color.from_str('#ffdd70'),
            description="📜**__Overview:__**"
            )
    reg_time = data['registered']
    dominance = data['dominance']
    pronouns = data['pronouns']
    sexuality = data['sexuality']
    embed.add_field(name="Dominance:", value=f'`{dominance}`', inline=True)
    embed.add_field(name="Pronouns:", value=f'`{pronouns}`', inline=True)
    embed.add_field(name="Sexuality:", value=f'`{sexuality}`', inline=True)
    embed.add_field(name="Registered on:", value=f'<t:{reg_time}>', inline=True)
    embed.set_thumbnail(url = mem.avatar.url)
    await inter.response.send_message(embed=embed)

bot.add_command(gag)
bot.add_command(ungag)
bot.add_command(register)
bot.add_command(profile)
aclient.run(token=config['bot']['token'])

