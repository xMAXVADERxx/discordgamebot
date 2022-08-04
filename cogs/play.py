import discord
from discord.ext import commands

class Play(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @commands.command(name="tictactoe",aliases=["ttt","nc"])
    async def tictactoe(self, ctx):
        await ctx.send("WIP!") 
    
    @commands.command(name="ConnectFour",aliases=["c4","connect"])
    async def connectfour(self, ctx):
        await ctx.send("WIP!")
        grid = [['E','E','E','E','E','E','E','E','E'],['E','E','E','E','E','E','E','E','E'],['E','E','E','E','E','E','E','E','E'],['E','E','E','E','E','E','E','E','E'],['E','E','E','E','E','E','E','E','E'],['E','E','E','E','E','E','E','E','E'],['E','E','E','E','E','E','E','E','E'],['E','E','E','E','E','E','E','E','E'],['E','E','E','E','E','E','E','E','E']]
        msg = ""
        for row in grid:
            for chr in row:
                msg += chr
            msg += '\n'
        await ctx.send(msg)
    
def setup(bot):
    bot.add_cog(Play(bot))

