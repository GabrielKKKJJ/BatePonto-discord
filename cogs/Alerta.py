import discord
from discord.ext import commands
from discord.ui import View, button
from discord import app_commands
from cogs.Config import get_channels, get_roles



class AlertaCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def  on_ready(self):
        print("Alerta cog carregado")

    async def has_any_role(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator: return True

        user_role_ids = [role.id for role in interaction.user.roles]

        allowed_role_ids = await get_roles(interaction.guild.name)

        has_role = any(role_id in user_role_ids for role_id in allowed_role_ids)

        return has_role
    
    @app_commands.command(description="ALERTA")
    async def alerta(self, interaction: discord.Interaction, title: str, message: str):
        try:
            if not await self.has_any_role(interaction):
                return await interaction.response.send_message("Sem permissão", ephemeral=True)
            
            channel_id = await get_channels(server_name=interaction.guild.name, channel_type='alert')

            if channel_id == None:
                return await interaction.response.send_message("Nenhum canal de alerta configurado", ephemeral=True)
            
            channel = self.bot.get_channel(channel_id)
            
            embed = discord.Embed(title=":rotating_light: ALERTA", color=discord.Color.red())
            embed.add_field(name=f"{title}", value=f"{message} \n @everyone", inline=False)
            
            await channel.send(embed=embed)

            await interaction.response.send_message("Alerta enviado", ephemeral=True)

        except Exception as e:
            print(e)

async def setup(bot):
    await bot.add_cog(AlertaCog(bot))
