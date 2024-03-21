import discord
from discord.ext import commands
from discord.ui import View, button
from discord import app_commands
import utils.DateOperations as DateOperations
import Firebase.DatabaseOperations as DatabaseOperations

# ID do cargo que pode iniciar o ponto
allowed_role_id = [941815669413007428, 941815669413007426, 941815669413007425, 941815669413007425, 941815669413007424, 941815669413007423, 941815669413007422, 941815669413007421]  # ID do cargo que pode iniciar o ponto

class MenuPonto(View):
    def __init__(self, embed, ponto_ParaCalcular, hourToCalc):
        super().__init__()
        self.value = None
        self.embed = embed
        self.ponto_ParaCalcular = ponto_ParaCalcular
        self.hourToCalc = hourToCalc
        self.pause_start = None
        self.total_time = 0

    @button(label="Parar", style=discord.ButtonStyle.red)
    async def menu1(self, interaction, button):
        try:
            date_operations = DateOperations.DateTimeConverter(interaction=interaction)

            ponto_final = await date_operations.date()
            hour = await date_operations.hours()

            if self.total_time == 0:
                total_time = await date_operations.dateCalculate(self.ponto_ParaCalcular, self.hourToCalc)
            else:
                total_time = await date_operations.dateCalculate(self.ponto_ParaCalcular, self.hourToCalc, self.total_time)

            self.embed.add_field(name=f"Ponto finalizado as:", value=f"`{ponto_final} as {hour}`", inline=False)
            self.embed.add_field(name="Tempo total:", value=f"{total_time['hours']} Horas, {total_time['minutes']} Minutos, {total_time['seconds']}, Segundos", inline=False)

            to_register = {
                "User": interaction.user.name,
                "Date": ponto_final,
                "Hours": total_time['hours'],
                "Minutes": total_time['minutes'],
                "Seconds": total_time['seconds'],
            }

            db = DatabaseOperations.DatabaseOperations()
            
            await db.register(register=to_register)
            await interaction.response.edit_message(embed=self.embed, view=None)

        except Exception as e:
            print(e)

    @button(label="Pausar", style=discord.ButtonStyle.grey)
    async def menu2(self, interaction, button):

        if(button.label=="Pausar"):
            self.pause_start = interaction.created_at
            date_operations = DateOperations.DateTimeConverter(interaction=interaction)
            
            ponto_pausa = await date_operations.date()
            hour = await date_operations.hours()

            self.embed.add_field(name=f"Ponto pausado:", value=f"`{ponto_pausa} as {hour}`", inline=False)
            button.style=discord.ButtonStyle.green
            button.label="Continuar"

            await interaction.response.edit_message(embed=self.embed, view=self)

        elif(button.label=="Continuar"):

            pause_end = interaction.created_at
        
            self.total_time += (pause_end - self.pause_start ).total_seconds()
            date_operations = DateOperations.DateTimeConverter(interaction=interaction)

            ponto_volta = await date_operations.date()
            hour = await date_operations.hours()

            self.embed.add_field(name="Voltou as:", value=f"`{ponto_volta} as {hour}`", inline=False)

            button.style=discord.ButtonStyle.grey
            button.label="Pausar"

            await interaction.response.edit_message(embed=self.embed, view=self)


class PontoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ponto cog carregado")

    @commands.has_any_role(941815669413007428, 941815669413007426, 941815669413007425, 941815669413007424, 941815669413007423, 941815669413007422, 941815669413007421)
    @app_commands.command(description="Inicia o ponto do usuario")
    async def ponto(self, interaction: discord.Interaction):
        date_operations = DateOperations.DateTimeConverter(interaction=interaction)
        ponto_inicial = await date_operations.date()
        hour = await date_operations.hours()

        embed = discord.Embed(title=":file_folder: Bate ponto", color=discord.Color.dark_embed())
        embed.add_field(name="Usuario", value=f"{interaction.user.mention}", inline=False)
        embed.add_field(name=f"Ponto iniciado as:", value=f"`{ponto_inicial} as {hour}`")

        viewPonto = MenuPonto(embed=embed, ponto_ParaCalcular=ponto_inicial, hourToCalc=hour)
        await interaction.response.send_message(embed=embed, view=viewPonto)
    
    @app_commands.command(description="Faz relatorio de pontos dos Staffs")
    async def relatorio(self, interaction: discord.Interaction):
        db = DatabaseOperations.DatabaseOperations()
        relatorio = await db.relatorio()

        embed = discord.Embed(title=":file_folder: Relatorio de Ponto",description="A meta de 20 horas semanais",color=discord.Color.dark_embed())
        for user in relatorio:
            embed.add_field(name=user["User"], value=f"{user['Hours']} Horas, {user['Minutes']} Minutos, {user['Seconds']} Segundos", inline=False)

        await interaction.response.send_message(embed=embed)
    
    @app_commands.command(description="Limpar banco de dados")
    async def cleardb(self, interaction: discord.Interaction):
        try:
            db = DatabaseOperations.DatabaseOperations()
            await db.cleardb()
            await interaction.response.send_message("Banco de dados limpo")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(PontoCog(bot))
