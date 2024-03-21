import asyncio
import os
import discord
from discord.ext import commands

# Define intents for bot functionality
intents = discord.Intents.default()

# Create a bot instance
bot = commands.Bot(command_prefix="$", intents=intents)

# Event for when the bot is ready
@bot.event
async def on_ready():
    """
    Called when the bot has successfully connected to Discord.
    Syncs application commands and prints a connection message.
    """
    await bot.tree.sync()  # Sync application commands with Discord
    print(f"{bot.user} se conectou ao discord")

# Event for handling command errors
@bot.event
async def on_command_error(ctx, error):
    """
    Handles errors raised during command execution.
    Sends a message if an invalid command is used.
    """
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado.")

# Function to load cogs (extensions containing commands)
async def load_cogs():
    """
    Loads all cogs located in the './cogs' directory.
    """
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# Main function to start the bot
async def main():
    """
    Starts the bot and loads cogs.
    """
    async with bot:  # Context manager for proper shutdown
        await load_cogs()  # Load cogs before starting
        await bot.start("TOKEN")  # Replace with your bot token

asyncio.run(main())  # Start the bot
