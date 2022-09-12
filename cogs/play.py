import discord
from discord.ext import commands
import sqlite3

#handles the storing and management of games
class GamesContainer:
    
    #init sqlite
    con = sqlite3.connect("games.db")
    cursor = con.cursor()


    tttIds = []
    tttGrids = []
    
    def __init__(self):
        print("Initialised Container")

    def addGame(self, gameID, gameType, gameGrid):
        if gameType == "ttt":
            self.tttIds.append(gameID)
            self.tttGrids.append(gameGrid)

        return
    def grabGame(self, gameID):
        return
      
Container = GamesContainer()

class Play(commands.Cog):
    
    
    def __init__(self,bot):
        self.bot = bot
        
    @commands.command(name="tictactoe",aliases=["ttt","nc"])
    async def tictactoe(self, ctx):
        await ctx.send("WIP!") 
        grid = [[0,0,0],[0,0,0],[0,0,0]]
        msg = ""
        for row in grid:
            for chr in row:
                if chr == 0:
                    msg += ":white_large_square:"
                elif chr == 1:
                    msg += ":negative_squared_cross_mark:"
                else:
                    msg += ":white_square_button:"
            msg += '\n'
        embedVar = discord.Embed(title="TicTacToe", description=f"{msg}")
        id = await ctx.channel.send(embed=embedVar)
        print(id)
        #store ID in array
        Container.addGame(gameID=id, gameType="ttt", gameGrid=grid)

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

