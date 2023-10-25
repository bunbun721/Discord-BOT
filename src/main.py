from discord.ext import commands
import discord

import random
import requests
import asyncio

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

@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    if reason is None:
        ban_reason = [
            "Bad bunbun",
            "Bye bye bun :wave:",
        ]
        await ctx.send(f'{random.choice(ban_reason)} {member.mention}')
    else:
        await ctx.send(f'{reason} {member.mention}')
    await member.ban(reason=reason)

@bot.command()
async def xkcd(ctx):
    image_link = "https://xkcd.com/" + str(random.randint(1, 1000)) + "/info.0.json"
    get_image = requests.get(image_link)
    image = get_image.json()
    await ctx.send(image["img"])

@bot.command()
async def poll(ctx, question, time_limit=0):
    bot_question = await ctx.send("@here " + question)
    await bot_question.add_reaction("👍")
    await bot_question.add_reaction("👎")

    if time_limit > 0:
        await ctx.send("Time limit is " + str(time_limit) + " seconds")
        await asyncio.sleep(time_limit)
        question_result = await ctx.channel.fetch_message(bot_question.id)
        await ctx.send("The results for ***" + question + "*** are :\n- 👍 : " + str(question_result.reactions[0].count - 1) + "\n- 👎 : " + str(question_result.reactions[1].count - 1))
        await bot_question.delete()

token = os.getenv('TOKEN')
bot.run(token)  # Starts the bot