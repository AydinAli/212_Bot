import discord

with open("token.txt", "r") as token_file:
  TOKEN = token_file.read()

intents = discord.Intents.all()

from discord.ext import commands
prefix = "!"
bot = commands.Bot(command_prefix = prefix, intents = intents)

@bot.command()
async def hello(ctx):
  await ctx.send("Hello!")

bot.run(TOKEN)