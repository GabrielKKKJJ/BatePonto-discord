import discord
from discord.ext import commands
from discord.ui import View, button
from discord import app_commands
from discord.ui.item import Item
import config.db_config as server_config

class ConfigView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(ConfigSelect())

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item) -> None:
        print(f"Error in view: {error}")

class ConfigSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                emoji="🚨",
                label="Alerta",
                description="Configure o canal de alerta"
            ),
            discord.SelectOption(
                emoji="📁",
                label="Ponto",
                description="Configure o canal de ponto"
            ),
            discord.SelectOption(
                emoji="📜",
                label="Permissões",
                description="Configure quem pode usar o bot"
            )
        ]
        super().__init__(
            placeholder="⚙️ Configurações",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "Alerta":
            self.view.clear_items()

            channel_view = ChannelView(modal='Alerta')

            await interaction.response.edit_message(content="Selecione o canal de alerta:", view=channel_view)

        elif self.values[0] == "Ponto":
            self.view.clear_items()
            
            channel_view = ChannelView(modal='Ponto')

            await interaction.response.edit_message(content="Selecione o canal de ponto:", view=channel_view)
        elif self.values[0] == "Permissões":
            self.view.clear_items()

            permissions_view = PermissionsView()

            await interaction.response.edit_message(content="Selecione quem pode usar o bot:", view=permissions_view)

class ChannelView(discord.ui.View):
    def __init__(self, modal = None):
        super().__init__()
        self.add_item(ChannelSelect(modal = modal))

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item) -> None:
        print(f"Error in view: {error}")

class ChannelSelect(discord.ui.ChannelSelect):
    def __init__(self, modal=None):
        self.modal = modal
        super().__init__(
            placeholder="Selecione o canal",
            min_values=1,
            max_values=1
        )

    async def callback(self, interaction: discord.Interaction):
        if self.modal != None:
            if self.modal == 'Alerta':
                channel = self.values[0]
                channel_id = channel.id

                await server_config.ServerConfig().update_config(server_name=interaction.guild.name, field = 'channels.alert', config={'channels.alert': channel_id})  # usa o ID do canal selecionado para atualizar a configuração
                await interaction.response.send_message(f"Canal de alerta definido para: {channel.mention}")  # menciona o canal selecionado na mensagem de resposta

            elif self.modal == 'Ponto':
                channel = self.values[0]
                channel_id = channel.id

                await server_config.ServerConfig().update_config(server_name=interaction.guild.name, field='channels.ponto', config={'channels.ponto': channel_id})  # usa o ID do canal selecionado para atualizar a configuração
                await interaction.response.send_message(f"Canal de ponto definido para: {channel.mention}")  # menciona o canal selecionado na mensagem de resposta

class PermissionsView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(PermissionsSelect())

    async def on_error(self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item) -> None:
        print(f"Error in view: {error}")

class PermissionsSelect(discord.ui.RoleSelect):
    def __init__(self):
        super().__init__(
            placeholder="Selecione os cargos",
            min_values=1,
            max_values=25, 
        )
    async def callback(self, interaction: discord.Interaction):
        roles = self.values
        roles_list = []
        for role in roles:
            role_id = role.id
            roles_list.append(role_id)
        await server_config.ServerConfig().update_config(server_name=interaction.guild.name, field='permissions', config={'permissions': roles_list})
        await interaction.response.send_message("Permissoes atualizadas")

async def get_roles(server_name: str):
    try:
        config = await server_config.read_json(f'config/Servers_configs/{server_name}/config.json')
        return config['permissions']

    except Exception as e:
        print("Error while getting roles:", e)

async def get_channels(server_name: str, channel_type):
    try:
        config = await server_config.read_json(f'config/Servers_configs/{server_name}/config.json')
        channels = config['channels']

        for channel in channels:
            if channel_type == 'alert':
                if channel == 'alert':
                    return channels[channel]
            elif channel_type == 'ponto':
                if channel == 'ponto':
                    return channels[channel]
        
    except Exception as e:
        print("Error while getting channels:", e)


class ConfigCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Config cog carregado")


    @app_commands.command(description="Configura o bot")
    async def config(self, interaction: discord.Interaction):
        try:
            if not await self.has_any_role(interaction):
                return await interaction.response.send_message("Sem permissão", ephemeral=True)
            
            await server_config.ServerConfig().initialize_config(interaction.guild.name)
            view = ConfigView()
            await interaction.response.send_message(view=view)
            
        except Exception as e:
            print(e)
    
    async def has_any_role(self, interaction: discord.Interaction):
        if interaction.user.guild_permissions.administrator: return True

        user_role_ids = [role.id for role in interaction.user.roles]

        allowed_role_ids = await get_roles(interaction.guild.name)

        has_role = any(role_id in user_role_ids for role_id in allowed_role_ids)

        return has_role

async def setup(bot):
    await bot.add_cog(ConfigCog(bot))