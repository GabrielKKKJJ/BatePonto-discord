import discord
from discord.ext import commands
from discord.ui import View, button
from discord import app_commands
import utils.DateOperations as DateOperations
import Firebase.db_ponto as db_ponto
from cogs.Config import get_channels, get_roles
from Firebase.firebase_init import init_firebase

class MenuPonto(View):
    def __init__(self, embed, initial_date, initial_hour, timeout=None):
        super().__init__(timeout=timeout)
        self.value = None
        self.embed = embed
        self.initial_date = initial_date
        self.initial_hour = initial_hour
        self.pause_start = None
        self.total_time = 0
        self.is_paused = False
        self.pause_hour = None
        self.pause_date = None

    @button(label="Parar", style=discord.ButtonStyle.red)
    async def stop(self, interaction, button):
        try:
            print("Ponto finalizado")
            date_operations = DateOperations.DateTimeConverter(interaction=interaction)

            final_date = await date_operations.date()
            hour = await date_operations.hours()

            if self.is_paused:
                total_time = await self._calculate_time_with_pause(date_operations, self.initial_date, self.initial_hour, self.pause_date, self.pause_hour, self.total_time)
            else:
                total_time = await self._calculate_time_without_pause(date_operations, self.initial_date, self.initial_hour, final_date, hour, self.total_time)

            self.embed.add_field(name=f"Ponto finalizado as:", value=f"`{final_date} as {hour}`", inline=False)
            self.embed.add_field(name="Tempo total:", value=f"{total_time['hours']} Horas, {total_time['minutes']} Minutos, {total_time['seconds']}, Segundos", inline=False)

            to_register = {
                "User": interaction.user.name,
                "Date": final_date,
                "Hours": total_time['hours'],
                "Minutes": total_time['minutes'],
                "Seconds": total_time['seconds'],
            }

            db = db_ponto.DatabaseOperations()
            await db.register(server_name=interaction.guild.name, register=to_register)
            await interaction.response.edit_message(embed=self.embed, view=None)

        except Exception as e:
            print(e)

    @button(label="Pausar", style=discord.ButtonStyle.grey)
    async def pause(self, interaction, button):
        if button.label == "Pausar":
            self.is_paused = True
            self.pause_start = interaction.created_at
            date_operations = DateOperations.DateTimeConverter(interaction=interaction)

            pause_date = await date_operations.date()
            hour = await date_operations.hours()

            self.pause_date = pause_date
            self.pause_hour = hour

            self.embed.add_field(name=f"Ponto pausado:", value=f"`{pause_date} as {hour}`", inline=False)
            button.style = discord.ButtonStyle.green
            button.label = "Continuar"

        elif button.label == "Continuar":
            self.is_paused = False
            pause_end = interaction.created_at
            self.total_time += (pause_end - self.pause_start).total_seconds()
            date_operations = DateOperations.DateTimeConverter(interaction=interaction)

            resume_date = await date_operations.date()
            hour = await date_operations.hours()

            self.embed.add_field(name="Voltou as:", value=f"`{resume_date} as {hour}`", inline=False)
            button.style = discord.ButtonStyle.grey
            button.label = "Pausar"

        await interaction.response.edit_message(embed=self.embed, view=self)

    async def _calculate_time_with_pause(self, date_operations, initial_date, initial_hour, pause_date, pause_hour, pause_time):
        if pause_time == 0:
            total_time = await date_operations.dateCalculate(initial_date, initial_hour, pause_date, pause_hour)
        else:
            total_time = await date_operations.dateCalculate(initial_date, initial_hour, pause_date, pause_hour, pause_time=pause_time)
        return total_time

    async def _calculate_time_without_pause(self, date_operations, initial_date, initial_hour, final_date, hour, total_time):
        if total_time == 0:
            total_time = await date_operations.dateCalculate(initial_date, initial_hour, final_date, hour)
        else:
            total_time = await date_operations.dateCalculate(initial_date, initial_hour, final_date, hour, pause_time=total_time)
        return total_time

class PontoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Ponto cog carregado")

    async def has_any_role(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator:
            return True

        user_role_ids = [role.id for role in interaction.user.roles]
        allowed_role_ids = await get_roles(interaction.guild.name)
        has_role = any(role_id in user_role_ids for role_id in allowed_role_ids)

        return has_role

    @app_commands.command(description="Inicia o ponto do usuario")
    async def ponto(self, interaction: discord.Interaction):
        try:
            if not await self.has_any_role(interaction):
                return await interaction.response.send_message("Nao tem permissao para usar este comando", ephemeral=True)

            channel_id = await get_channels(server_name=interaction.guild.name, channel_type='ponto')
            if channel_id is None:
                return await interaction.response.send_message("Nenhum canal de ponto configurado", ephemeral=True)

            channel = self.bot.get_channel(channel_id)

            if channel != interaction.channel:
                return await interaction.response.send_message(f"Este comando pode ser usado apenas no canal {channel.mention} ", ephemeral=True)

            date_operations = DateOperations.DateTimeConverter(interaction=interaction)
            initial_date = await date_operations.date()
            initial_hour = await date_operations.hours()

            embed = discord.Embed(title=":file_folder: Bate ponto", color=discord.Color.dark_embed())
            embed.add_field(name="Usuario", value=f"{interaction.user.mention}", inline=False)
            embed.add_field(name=f"Ponto iniciado as:", value=f"`{initial_date} as {initial_hour}`")

            view_ponto = MenuPonto(embed=embed, initial_date=initial_date, initial_hour=initial_hour, timeout=None)
            await interaction.response.send_message(embed=embed, view=view_ponto)

        except Exception as e:
            print(e)

    @app_commands.command(description="Faz relatorio de pontos dos Staffs")
    async def relatorio(self, interaction: discord.Interaction):
        try:
            if not await self.has_any_role(interaction):
                return await interaction.response.send_message("Nao tem permissao para usar este comando", ephemeral=True)

            channel_id = await get_channels(server_name=interaction.guild.name, channel_type='ponto')
            if channel_id is None:
                return await interaction.response.send_message("Nenhum canal de ponto configurado", ephemeral=True)

            channel = self.bot.get_channel(channel_id)

            if channel != interaction.channel:
                return await interaction.response.send_message(f"Este comando pode ser usado apenas no canal {channel.mention}", ephemeral=True)

            db = db_ponto.DatabaseOperations()
            relatorio = await db.relatorio(server_name=interaction.guild.name)

            embed = discord.Embed(title=":file_folder: Relatorio de Ponto", description="A meta de 12 horas semanais", color=discord.Color.dark_embed())
            for user in relatorio:
                if user['Hours'] >= 12:
                    embed.add_field(name=f":green_circle: {user['User']}", value=f"{user['Hours']} Horas, {user['Minutes']} Minutos, {user['Seconds']} Segundos", inline=False)

                elif user['Hours'] >= 6:
                    embed.add_field(name=f":yellow_circle: {user['User']}", value=f"{user['Hours']} Horas, {user['Minutes']} Minutos, {user['Seconds']} Segundos", inline=False)

                elif user['Hours'] < 6:
                    embed.add_field(name=f":red_circle: {user['User']}", value=f"{user['Hours']} Horas, {user['Minutes']} Minutos, {user['Seconds']} Segundos", inline=False)

            await interaction.response.send_message(embed=embed)

        except Exception as e:
            print(e)

    @app_commands.command(description="Limpar banco de dados")
    async def cleardb(self, interaction: discord.Interaction):
        try:
            if not await self.has_any_role(interaction):
                return await interaction.response.send_message("Nao tem permissao para usar este comando", ephemeral=True)

            channel_id = await get_channels(server_name=interaction.guild.name, channel_type='ponto')
            if channel_id is None:
                return await interaction.response.send_message("Nenhum canal de ponto configurado", ephemeral=True)

            channel = self.bot.get_channel(channel_id)

            if channel != interaction.channel:
                return await interaction.response.send_message(f"Este comando pode ser usado apenas no canal {channel.mention}", ephemeral=True)

            db = db_ponto.DatabaseOperations()
            await db.cleardb(server_name=interaction.guild.name)

            await interaction.response.send_message("Relatorios limpos")
        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(PontoCog(bot))
