import discord
import json
from discord.ext import commands
from cogs.account import AccountManager
extensions = ['cogs.play','cogs.account']

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
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix=check_prefix, case_insensitive=True, intents=intents)
    
    #Feedback when active
    @bot.event
    async def on_ready():
        for extension in extensions:
            await bot.load_extension(extension)
        print(f"Current ID: {bot.user.id}")
        print("Bot Online!")
        
    #used to add an entire server to the database; slow implementation and so depricated
    # @bot.event
    # async def on_guild_join(guild):
    #     print(f"Joined {guild.name}, syncing database")
    #     Manager = AccountManager()
    #     for member in guild.members:
    #         Manager.checkAccount(member.id)

    @bot.hybrid_command(name="sync", description="Used to sync commands, only runable by owner")
    async def sync(ctx: commands.Context):
        if ctx.author.id == 274620118795812864:
            guild = ctx.guild
            bot.tree.copy_global_to(guild=guild)
            await bot.tree.sync()
            await ctx.send("Synced")

    bot.run(config["TOKEN"])
