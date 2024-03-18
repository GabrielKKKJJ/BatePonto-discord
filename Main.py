# This example requires the 'message_content' intent.

import discord
from discord.ext import commands
from discord_components import DiscordComponents, ComponentsBot, Button
import pytz

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='$', intents=intents)



@bot.command(description="Somar dois numeros")
async def somar(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(f"A soma dada por {ctx.author} é {left + right}")

@bot.command(description="Somar dois numeros")
async def contar(ctx, left: int, right: int):
    """Adds two numbers together."""
    for i in range(left, right+1):
        await ctx.send(f"{ctx.author} conta {i}")

ponto = None

class Menu(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Parar", style=discord.ButtonStyle.red)
    async def menu1(self, button: discord.ui.Button, interaction: discord.Interaction):
        fuso_origem = pytz.utc
        fuso_br = pytz.timezone('America/Sao_Paulo')
        time = interaction.created_at.replace(tzinfo=fuso_origem)
        time = time.astimezone(fuso_br)
        time = time.strftime("%H:%M - %d/%m/%Y")
        ponto_final = time
        await interaction.response.edit_message(content=f"{ponto} \n ponto finalizado as {ponto_final}")



@bot.command()
async def ponto(ctx):
    fuso_origem = pytz.utc
    fuso_br = pytz.timezone('America/Sao_Paulo')
    time = ctx.message.created_at.replace(tzinfo=fuso_origem)
    time = time.astimezone(fuso_br)
    time = time.strftime("%H:%M - %d/%m/%Y")

    global ponto
    view = Menu()
    await ctx.reply(f"Ponto iniciado as {time}", view=view)



bot.run('MTIxODgwMTYyMjAwODk4NzY3OQ.GhwEAi.kFTXSitCNJxCGU0WfF_P917_1zNiqWEpCtdejM')

