import discord
import re

lowt={'a': 'a', 'b': 'b', 'c': 'e', 'd': 'm', 'e': 'e', 'f': 'h', 'g': 'm', 'h': 'h', 'i': 'i', 'j': 'a', 'k': 'k', 'l': 'a', 'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'k', 'r': 'a', 's': 'z', 't': 'e', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'k', 'y': 'y', 'z': 's', 'A': 'A', 'B': 'B', 'C': 'E', 'D': 'M', 'E': 'E', 'F': 'H', 'G': 'M', 'H': 'H', 'I': 'I', 'J': 'A', 'K': 'K', 'L': 'A', 'M': 'M', 'N': 'N', 'O': 'O', 'P': 'P', 'Q': 'K', 'R': 'A', 'S': 'Z', 'T': 'E', 'U': 'U', 'V': 'V', 'W': 'W', 'X': 'K', 'Y': 'Y', 'Z': 'S'}
medt={'a': 'a', 'b': 'f', 'c': 'k', 'd': 'm', 'e': 'e', 'f': 'm', 'g': 'm', 'h': 'h', 'i': 'e', 'j': 'a', 'k': 'k', 'l': 'a', 'm': 'm', 'n': 'n', 'o': 'e', 'p': 'f', 'q': 'k', 'r': 'a', 's': 'h', 't': 'e', 'u': 'e', 'v': 'f', 'w': 'a', 'x': 'k', 'y': 'e', 'z': 'h', 'A': 'A', 'B': 'F', 'C': 'K', 'D': 'M', 'E': 'E', 'F': 'M', 'G': 'M', 'H': 'H', 'I': 'E', 'J': 'A', 'K': 'K', 'L': 'A', 'M': 'M', 'N': 'N', 'O': 'E', 'P': 'F', 'Q': 'K', 'R': 'A', 'S': 'H', 'T': 'E', 'U': 'E', 'V': 'F', 'W': 'A', 'X': 'K', 'Y': 'E', 'Z': 'H'}
higt={'a': 'e', 'b': 'b', 'c': 'm', 'd': 'm', 'e': 'e', 'f': 'm', 'g': 'm', 'h': 'h', 'i': 'e', 'j': 'a', 'k': 'a', 'l': 'a', 'm': 'm', 'n': 'm', 'o': 'e', 'p': 'm', 'q': 'm', 'r': 'a', 's': 'h', 't': 'm', 'u': 'e', 'v': 'm', 'w': 'm', 'x': 'm', 'y': 'e', 'z': 'h', 'A': 'E', 'B': 'B', 'C': 'M', 'D': 'M', 'E': 'E', 'F': 'M', 'G': 'M', 'H': 'H', 'I': 'E', 'J': 'A', 'K': 'A', 'L': 'A', 'M': 'M', 'N': 'M', 'O': 'E', 'P': 'M', 'Q': 'M', 'R': 'A', 'S': 'H', 'T': 'M', 'U': 'E', 'V': 'M', 'W': 'M', 'X': 'M', 'Y': 'E', 'Z': 'H'}
tight={'a': 'm', 'b': 'm', 'c': 'm', 'd': 'm', 'e': 'm', 'f': 'm', 'g': 'm', 'h': 'm', 'i': 'm', 'j': 'm', 'k': 'm', 'l': 'm', 'm': 'm', 'n': 'm', 'o': 'm', 'p': 'm', 'q': 'm', 'r': 'm', 's': 'm', 't': 'm', 'u': 'm', 'v': 'm', 'w': 'm', 'x': 'm', 'y': 'm', 'z': 'm', 'A': 'm', 'B': 'm', 'C': 'm', 'D': 'm', 'E': 'm', 'F': 'm', 'G': 'm', 'H': 'm', 'I': 'm', 'J': 'm', 'K': 'm', 'L': 'm', 'M': 'm', 'N': 'm', 'O': 'm', 'P': 'm', 'Q': 'm', 'R': 'm', 'S': 'm', 'T': 'm', 'U': 'm', 'V': 'm', 'W': 'm', 'X': 'm', 'Y': 'm', 'Z': 'm'}
lvls={'lowt':lowt,'medt':medt,'higt':higt,'tight':tight}

def preprocess(msg:discord.Message):
    ...

def gag(msg:str, intensity:str, charset:dict=None) -> str:
    cont=msg.content
    if cont=='':
        return
    tlvl=intensity
    l=re.findall(r'\*[^\*]+\*', cont)
    j=re.findall(r'_[^_]+_', cont)
    for lvl in lvls:
        if tlvl==lvl:
            for key in lvls[lvl]:
                cont=cont.replace(key, lvls[lvl][key])
    l1=re.findall(r'\*[^\*]+\*', cont)
    j1=re.findall(r'_[^_]+_', cont)
    for i in range(len(l)):
        cont=cont.replace(l1[i], l[i])
    for i in range(len(j)):
        cont=cont.replace(j1[i], j[i])
    cont = re.sub(r'<@&\d+>', '(@)some role', cont)
    return cont

async def websend(msg:discord.Message, client:discord.Client, cont:str=None, del_prev:bool=False):
    """
    Sends a webhook message in the channel of the `msg` object
    Args:
        msg: The discord.Message object from the on_message event
        client: The bot object
        cont: The content you wish to send the webhook msg, defaults to content form the original msg 
    """

    if not cont:
        cont=msg.content 
    wlist= await msg.channel.webhooks()
    webh=None
    if not wlist:
        webh=await msg.channel.create_webhook(name='Kigamuri Mask')
    else:
        for web in wlist:
            if web.user.name==client.user.name:
                webh=web
                break

        if webh == None:
            webh=await msg.channel.create_webhook(name='Kigurumi Mask')

    if msg.attachments:
        da_files=[]
        for a in msg.attachments:
            file=await a.to_file()
            da_files.append(file)

    if del_prev:
        await msg.delete()

    await webh.send(cont, avatar_url=msg.author.avatar.url, username=f"{msg.author.display_name}")
    if msg.attachments:
        await webh.send(files=da_files, avatar_url=msg.author.avatar.url, username=f"{msg.author.display_name}")
    

