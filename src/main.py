from discord.ext import commands
import discord

import random

import os
from dotenv import load_dotenv
load_dotenv()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(
    command_prefix="!",  # Change to desired prefix
    case_insensitive=True, # Commands aren't case-sensitive
    intents = intents # Set up basic permissions
)

bot.author_id = 372823346007506955 # Change to your discord id

@bot.event
async def on_ready():  # When the bot is ready
    print("I'm in")
    print(bot.user)  # Prints the bot's username and identifier

@bot.command()
async def pong(ctx):
    await ctx.send('pong')

@bot.command()
async def name(ctx):
    await ctx.send(ctx.author.name)

@bot.command()
async def d6(ctx):
    await ctx.send(random.randint(1,6))

@bot.event
async def on_message(message):
    if message.content == "Salut tout le monde":
        await message.channel.send("Salut tout seul " + message.author.mention)
    await bot.process_commands(message)

@bot.command()
async def admin(ctx, member: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Admin")
    if not role:
        await ctx.guild.create_role(name="Admin", permissions=discord.Permissions(8))
    await member.add_roles(role)
    await ctx.send("Congrats " + member.mention + " ! You are now an admin !")

token = os.getenv('TOKEN')
bot.run(token)  # Starts the bot