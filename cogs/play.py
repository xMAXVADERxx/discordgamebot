import discord
from discord.ext import commands

class Play(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name="tictactoe",aliases=["ttt","nc"])
    async def tictactoe(self, ctx):
        await ctx.send("WIP!")

def setup(bot):
    bot.add_cog(Play(bot))

