import discord
import json
from discord.ext import commands
from dotenv import load_dotenv
import os

extensions = ['cogs.play']

def check_prefix(bot, msg):
    base = ["g!"]
    return base

#Dunder, because it looks nice
if __name__ == "__main__":



    #Loading config (stored in a .env for Heroku support)
    load_dotenv()
    TOKEN = os.getenv("TOKEN")

    #define bot
    bot = commands.Bot(command_prefix=check_prefix, case_insensitive=True)
    
    for extension in extensions:
        bot.load_extension(extension)
    #Feedback when active
    @bot.event
    async def on_ready():
        print("Bot Online!")

    bot.run(TOKEN)
