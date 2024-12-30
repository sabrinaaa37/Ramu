import discord
import re
from discord import ui, app_commands
import pyrebase
from utils.messages import *

lowt={'a': 'a', 'b': 'b', 'c': 'e', 'd': 'm', 'e': 'e', 'f': 'h', 'g': 'm', 'h': 'h', 'i': 'i', 'j': 'a', 'k': 'k', 'l': 'a', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'k', 'r': 'a', 's': 'z', 't': 'e', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'k', 'y': 'y', 'z': 's', 'A': 'A', 'B': 'B', 'C': 'E', 'D': 'M', 'E': 'E', 'F': 'H', 'G': 'M', 'H': 'H', 'I': 'I', 'J': 'A', 'K': 'K', 'L': 'A', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'K', 'R': 'A', 'S': 'Z', 'T': 'E', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'K', 'Y': 'Y', 'Z': 'S'}
medt={'a': 'a', 'b': 'f', 'c': 'k', 'd': 'm', 'e': 'e', 'f': 'm', 'g': 'm', 'h': 'h', 'i': 'e', 'j': 'a', 'k': 'k', 'l': 'a', 'm': 'm', 'n': 'n', 'o': 'e', 'p': 'f', 'q': 'k', 'r': 'a', 's': 'h', 't': 'e', 'u': 'e', 'v': 'f', 'w': 'a', 'x': 'k', 'y': 'e', 'z': 'h', 'A': 'A', 'B': 'F', 'C': 'K', 'D': 'M', 'E': 'E', 'F': 'M', 'G': 'M', 'H': 'H', 'I': 'E', 'J': 'A', 'K': 'K', 'L': 'A', 'M': 'M', 'N': 'N', 'O': 'E', 'P': 'F', 'Q': 'K', 'R': 'A', 'S': 'H', 'T': 'E', 'U': 'E', 'V': 'F', 'W': 'A', 'X': 'K', 'Y': 'E', 'Z': 'H'}
higt={'a': 'e', 'b': 'b', 'c': 'm', 'd': 'm', 'e': 'e', 'f': 'm', 'g': 'm', 'h': 'h', 'i': 'e', 'j': 'a', 'k': 'a', 'l': 'a', 'm': 'm', 'n': 'm', 'o': 'e', 'p': 'm', 'q': 'm', 'r': 'a', 's': 'h', 't': 'm', 'u': 'e', 'v': 'm', 'w': 'm', 'x': 'm', 'y': 'e', 'z': 'h', 'A': 'E', 'B': 'B', 'C': 'M', 'D': 'M', 'E': 'E', 'F': 'M', 'G': 'M', 'H': 'H', 'I': 'E', 'J': 'A', 'K': 'A', 'L': 'A', 'M': 'M', 'N': 'M', 'O': 'E', 'P': 'M', 'Q': 'M', 'R': 'A', 'S': 'H', 'T': 'M', 'U': 'E', 'V': 'M', 'W': 'M', 'X': 'M', 'Y': 'E', 'Z': 'H'}
tight={'a': 'm', 'b': 'm', 'c': 'm', 'd': 'm', 'e': 'm', 'f': 'm', 'g': 'm', 'h': 'm', 'i': 'm', 'j': 'm', 'k': 'm', 'l': 'm', 'm': 'm', 'n': 'm', 'o': 'm', 'p': 'm', 'q': 'm', 'r': 'm', 's': 'm', 't': 'm', 'u': 'm', 'v': 'm', 'w': 'm', 'x': 'm', 'y': 'm', 'z': 'm', 'A': 'm', 'B': 'm', 'C': 'm', 'D': 'm', 'E': 'm', 'F': 'm', 'G': 'm', 'H': 'm', 'I': 'm', 'J': 'm', 'K': 'm', 'L': 'm', 'M': 'm', 'N': 'm', 'O': 'm', 'P': 'm', 'Q': 'm', 'R': 'm', 'S': 'm', 'T': 'm', 'U': 'm', 'V': 'm', 'W': 'm', 'X': 'm', 'Y': 'm', 'Z': 'm'}
lvls={'lowt':lowt,'medt':medt,'higt':higt,'tight':tight}

intents = discord.Intents.default()
intents.message_content=True
intents.members=True

class client(discord.Client):
    def __init__(self,db:pyrebase.pyrebase.Database):
        super().__init__(intents=intents)
        self.synced = False
        self.type = type
        self.bot = app_commands.CommandTree(self)
        self.db = db
        self.cache = {}
    
    def fill_cache(self):
        ...

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await self.bot.sync()
            self.synced= True
        print(f"Logged in as {self.user}")
    
    async def on_message(self,msg:discord.Message):
        if msg.author.bot:
            return

        if self.db.child('guilds').child(msg.guild.id).child(msg.author.id).get().val():
            cont = gag(msg, 'lowt')
            await websend(msg,self,cont,True)