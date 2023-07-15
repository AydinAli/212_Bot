import discord
from discord.ext import commands
import matplotlib.pyplot as plt

import utilities

with open("token.txt", "r") as token_file:
  TOKEN = token_file.read()

intents = discord.Intents.all()
prefix = "!"
bot = commands.Bot(command_prefix = prefix, intents = intents)

@bot.event
async def on_ready():
  with open("equations_latex.txt", 'w') as file:
    pass

@bot.command()
async def hello(ctx):
  await ctx.send("Hello!")

@bot.command()
async def display(ctx, arg):
  image_filepath = utilities.create_eq_image(arg)
  with open(image_filepath, 'rb') as fp:
    await ctx.send(file=discord.File(fp, 'image.png'))

@bot.command()
async def create(ctx, arg): #Create a named equation (input will go somewhere else)
  if utilities.find_line("equations_latex.txt", arg) != -1:
    await ctx.send(f"Equation '{arg}' already exists. If you want to redefine the contents, please use '!define \"{arg}: definition \"'")
    return
  await ctx.send(f"Initializing Equation '{arg}'. Please write the contents of this equation with '!define \"{arg}: definition \"'")
  with open("equations_latex.txt", 'a') as file:
    file.write(arg + ":\n")

@bot.command()
async def delete(ctx, arg): #Delete an existing equation entirely from list
  line_num = utilities.find_line("equations_latex.txt", arg)
  if line_num == -1:
    await ctx.send(f"Equation '{arg}' does not exist, so it cannot be deleted. ")
    return
  utilities.delete_eq_by_line_num("equations_latex.txt", line_num)
  await ctx.send("Equation successfully deleted.")

@bot.command()
async def define(ctx, arg): #Define a named equation
  split_input = arg.split(":")
  if (len(split_input) != 2):
    await ctx.send("Please provide the name of the equation followed by a colon and space with its definition. Ex: '!define \"Equation Name: Equation Definition\"'")
    await ctx.send("Also note that colons in equation are not supported at this time")
    return
  eq_name, eq_def = split_input
  line_num = utilities.find_line("equations_latex.txt", eq_name)
  if line_num == -1:
    await ctx.send(f"{eq_name} not found. Please declare this equation first with '!create \"Equation Name\"' if you wish to define it.")
    return
  utilities.write_eq_def("equations_latex.txt", line_num, eq_name, eq_def)
  await ctx.send("Equation saved. Please review the below image and see if the definition looks correct:")
  image_filepath = utilities.create_eq_image(eq_def)
  with open(image_filepath, 'rb') as fp:
    await ctx.send(file=discord.File(fp, 'image.png'))

@bot.command()
async def view(ctx, arg): #Displays the named equation
  line_num = utilities.find_line("equations_latex.txt", arg)
  if line_num == -1:
    await ctx.send(f"{arg} not found. Please check the list of defined equations.")
    return
  with open("equations_latex.txt", 'r') as file:
    lines = file.readlines()
    if len(lines[line_num].split(":")) != 2:
      await ctx.send("This equation does not yet have a definition so it cannot be viewed. Please define it with 'define \"Equation Name: Equation Definition\"'")
      return
    eq_def = lines[line_num].split(":")[1][1:-1] #Needs to remove the space after the colon and the new line after end of the definition
  image_filepath = utilities.create_eq_image(eq_def)
  with open(image_filepath, 'rb') as fp:
    await ctx.send(file=discord.File(fp, 'image.png'))

@bot.command()
async def listequations(ctx): #Lists all the currently declared equations
  await ctx.send("Now listing all equations:")
  eq_string = ""
  with open("equations_latex.txt", 'r') as file:
    lines = file.readlines()
    for line in lines: eq_string += line
  await ctx.send(eq_string)

@bot.command(aliases = ["kill", "stop", "exit"])
@commands.is_owner()
async def close(ctx):
  await ctx.send("Going offline.")
  await bot.close()

bot.run(TOKEN)