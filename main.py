import discord
import json
from discord.ext import commands
import os

extensions = ['cogs.play']

def check_prefix(bot, msg):
    base = ["g!"]
    return base

#Dunder, for safety
if __name__ == "__main__":

    try:
        with open("config/cfg.json","r") as file:
            config = json.load(file)
            file.close()
        print(config)
    except FileNotFoundError:
        print("Config file doesn't exist, please run config.py")
    #define bot
    bot = commands.Bot(command_prefix=check_prefix, case_insensitive=True)
    
    for extension in extensions:
        bot.load_extension(extension)
    #Feedback when active
    @bot.event
    async def on_ready():
        print("Bot Online!")

    bot.run(config["TOKEN"])
