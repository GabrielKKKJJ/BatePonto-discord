import asyncio
import os
import discord
from discord.ext import commands


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"{bot.user} se conectou ao discord")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Comando não encontrado.")


async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

async def main():
    async with bot:
        await load_cogs()
        await bot.start("MTIxODgwMTYyMjAwODk4NzY3OQ.GAYSTI.a10vpK0XwMIvSeSWBRlI9TNXAW5v1xiRGXoPTo")

asyncio.run(main())