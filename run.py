from os import listdir
import sys
sys.path.append('..')
from discord.ext import commands

client = commands.Bot(command_prefix="^")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f":exclamation: Command not found.")

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


for filename in listdir('./cogs'):
    if filename.endswith('.py'):
        if filename[:-3] == "__init__": continue
        client.load_extension(f'cogs.{filename[:-3]}')

client.run("Your tocken here")