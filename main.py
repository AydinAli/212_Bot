import discord
from discord.ext import commands
import matplotlib.pyplot as plt

import utilities


with open("token.txt", "r") as token_file:
  TOKEN = token_file.read()

intents = discord.Intents.all()
prefix = "!"
bot = commands.Bot(command_prefix = prefix, intents = intents)

@bot.command()
async def hello(ctx):
  await ctx.send("Hello!")

@bot.command()
async def display(ctx, arg):
  image_filepath = utilities.create_eq_image(arg)
  with open(image_filepath, 'rb') as fp:
    await ctx.send(file=discord.File(fp, 'image.png'))


@bot.command(aliases = ["kill", "stop", "exit"])
@commands.is_owner()
async def close(ctx):
  await ctx.send("Going offline.")
  await bot.close()

bot.run(TOKEN)