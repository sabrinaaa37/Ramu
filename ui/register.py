import discord
from discord import ui, SelectOption
import time
from pyrebase.pyrebase import Database


class RegisterView(ui.View):
    def __init__(self, user:discord.User,db:Database):
        super().__init__()
        self.dominance = DominanceDrop()
        self.add_item(self.dominance)

        self.pronouns = PronounsDrop()
        self.add_item(self.pronouns)

        self.sexuality = SexualityDrop()
        self.add_item(self.sexuality)

        self.add_item(SubmitButton(self,user,db))

class DominanceDrop(ui.Select):
    def __init__(self):
        options=[
            SelectOption(label='Dominant'),
            SelectOption(label='Switch (Dom lean)'),
            SelectOption(label='Switch (Sub lean)'),
            SelectOption(label='Submissive')
        ]
        super().__init__(
            placeholder="Choose your dom orientation",
            min_values=1,
            max_values=1,
            options=options,
        )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

class PronounsDrop(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label='He/Him'),
            SelectOption(label='She/Her'),
            SelectOption(label='They/Them'),
            SelectOption(label='It/Its')
        ]
        super().__init__(
            placeholder="Choose your pronouns",
            min_values=1,
            max_values=1,
            options=options,
        )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

class SexualityDrop(ui.Select):
    def __init__(self):
        options = [
            SelectOption(label='Straight'),
            SelectOption(label='Gay'),
            SelectOption(label='Lesbian'),
            SelectOption(label='Bisexual'),
            SelectOption(label='Pansexual')
        ]
        super().__init__(
            placeholder="Choose your sexuality",
            min_values=1,
            max_values=1,
            options=options,
        )
    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()

class SubmitButton(ui.Button):
    def __init__(self, parent_view, user, db):
        super().__init__(label="Submit", style=discord.ButtonStyle.green)
        self.parent_view = parent_view
        self.user = user
        self.db = db

    async def callback(self, interaction: discord.Interaction):

        dominance = self.parent_view.dominance.values[0] if self.parent_view.dominance.values else None
        pronouns = self.parent_view.pronouns.values[0] if self.parent_view.pronouns.values else None
        sexuality = self.parent_view.sexuality.values[0] if self.parent_view.sexuality.values else None
        
        if not (dominance and pronouns and sexuality):
            await interaction.response.send_message("Please select one option in all dropdowns", ephemeral=True)
        
        embed = discord.Embed(
            title = f"__• Profile of {self.user.display_name}__",
            color=discord.Color.from_str('#ffdd70'),
            description="📜**__Overview:__**"
            )
        embed.add_field(name="Dominance:", value=f'`{self.parent_view.dominance.values[0]}`', inline=True)
        embed.add_field(name="Pronouns:", value=f'`{self.parent_view.pronouns.values[0]}`', inline=True)
        embed.add_field(name="Sexuality:", value=f'`{self.parent_view.sexuality.values[0]}`', inline=True)
        embed.add_field(name="Registered on:", value=f'<t:{int(time.time())}>', inline=True)
        embed.set_thumbnail(url = self.user.avatar.url)

        data = {}
        data['dominance'] = dominance
        data['pronouns'] = pronouns
        data['sexuality'] = sexuality

        self.db.child('members').child(self.user.id).child('profile').set(data)
        await interaction.response.defer()
        await interaction.channel.send(embed=embed)
        await interaction.message.delete()