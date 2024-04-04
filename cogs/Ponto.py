import discord
from discord.ext import commands
from discord.ui import View, button
from discord import app_commands
import utils.DateOperations as DateOperations
import Firebase.DatabaseOperations as DatabaseOperations

# ID do cargo que pode iniciar o ponto
allowed_role_id = [941815669413007428, 941815669413007426, 941815669413007425, 941815669413007425, 941815669413007424, 941815669413007423, 941815669413007422, 941815669413007421]  # ID do cargo que pode iniciar o ponto

class MenuPonto(View):
    def __init__(self, embed, Initial_Date, Initial_Hour, timeout=None):
        super().__init__(timeout=timeout)
        self.value = None
        self.embed = embed
        self.Initial_Date = Initial_Date
        self.Initial_Hour = Initial_Hour
        self.pause_start = None
        self.total_time = 0
        self.isPause = False
        self.Pause_hour = None
        self.Pause_date = None

    @button(label="Parar", style=discord.ButtonStyle.red)
    async def menu1(self, interaction, button):
        try:
            print("Ponto finalizado")
            date_operations = DateOperations.DateTimeConverter(interaction=interaction)

            ponto_final = await date_operations.date()
            hour = await date_operations.hours()

            if self.isPause:
                "Paused"
                if self.total_time == 0:
                    "Paused and continued"
                    total_time = await date_operations.dateCalculate(self.Initial_Date, self.Initial_Hour, self.Pause_date, self.Pause_hour)
                else:
                    "Paused, continued and paused again"
                    total_time = await date_operations.dateCalculate(self.Initial_Date, self.Initial_Hour, self.Pause_date, self.Pause_hour, pause_time=self.total_time)
            else:
                "Not paused"
                if self.total_time == 0:
                    "Not paused"
                    total_time = await date_operations.dateCalculate(self.Initial_Date, self.Initial_Hour, ponto_final, hour)
                else:
                    "Continued"
                    total_time = await date_operations.dateCalculate(self.Initial_Date, self.Initial_Hour, ponto_final, hour, pause_time=self.total_time)

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
            self.isPause = True
            self.pause_start = interaction.created_at
            date_operations = DateOperations.DateTimeConverter(interaction=interaction)
            
            ponto_pausa = await date_operations.date()
            hour = await date_operations.hours()

            self.Pause_date = ponto_pausa
            self.Pause_hour = hour

            self.embed.add_field(name=f"Ponto pausado:", value=f"`{ponto_pausa} as {hour}`", inline=False)
            button.style=discord.ButtonStyle.green
            button.label="Continuar"

            await interaction.response.edit_message(embed=self.embed, view=self)

        elif(button.label=="Continuar"):

            self.isPause = False
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
        try:
            channel = self.bot.get_channel(1220114985317826731)

            if channel != interaction.channel:
                return await interaction.response.send_message("Este comando pode ser usado apenas no canal #ponto", ephemeral=True)
            
            date_operations = DateOperations.DateTimeConverter(interaction=interaction)
            Initial_Date = await date_operations.date()
            Initial_Hour = await date_operations.hours()

            embed = discord.Embed(title=":file_folder: Bate ponto", color=discord.Color.dark_embed())
            embed.add_field(name="Usuario", value=f"{interaction.user.mention}", inline=False)
            embed.add_field(name=f"Ponto iniciado as:", value=f"`{Initial_Date} as {Initial_Hour}`")

            viewPonto = MenuPonto(embed=embed, Initial_Date=Initial_Date, Initial_Hour=Initial_Hour, timeout=None)
            await interaction.response.send_message(embed=embed, view=viewPonto)

        except Exception as e:
            print(e)
    @app_commands.command(description="Faz relatorio de pontos dos Staffs")
    async def relatorio(self, interaction: discord.Interaction):
        try:
            channel = self.bot.get_channel(1220114985317826731)

            if channel != interaction.channel:
                return await interaction.response.send_message("Este comando pode ser usado apenas no canal #ponto", ephemeral=True)
            
            db = DatabaseOperations.DatabaseOperations()
            relatorio = await db.relatorio()

            embed = discord.Embed(title=":file_folder: Relatorio de Ponto",description="A meta de 12 horas semanais",color=discord.Color.dark_embed())
            for user in relatorio:
                if user['Hours'] >= 12:
                    embed.add_field(name=f"{user['User']} :green_circle:", value=f"{user['Hours']} Horas, {user['Minutes']} Minutos, {user['Seconds']} Segundos", inline=False)
                
                elif user['Hours'] >= 6:
                    embed.add_field(name=f"{user['User']} :yellow_circle:", value=f"{user['Hours']} Horas, {user['Minutes']} Minutos, {user['Seconds']} Segundos", inline=False)
                    
                elif user['Hours'] < 6:
                    embed.add_field(name=f"{user['User']} :red_circle:", value=f"{user['Hours']} Horas, {user['Minutes']} Minutos, {user['Seconds']} Segundos", inline=False)

            await interaction.response.send_message(embed=embed)
            
        except Exception as e:
            print(e)
        
    @app_commands.command(description="Limpar banco de dados")
    async def cleardb(self, interaction: discord.Interaction):
        try:
            channel = self.bot.get_channel(1220114985317826731)

            if channel != interaction.channel:
                return await interaction.response.send_message("Este comando pode ser usado apenas no canal #ponto", ephemeral=True)
            
            db = DatabaseOperations.DatabaseOperations()
            await db.cleardb()
            await interaction.response.send_message("Banco de dados limpo")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(PontoCog(bot))
