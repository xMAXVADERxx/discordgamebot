#Visual Studio Stuff
from codecs import ignore_errors
from re import X

import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

#import local modules
from .games.enums import Games
from .account import AccountManager
from .games.tictactoe import Tictactoe

#handles the storing and management of games
class GamesContainer:
    
    #init sqlite
    con = sqlite3.connect("games.db")
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS games(gameID TEXT PRIMARY KEY, gameType INTEGER, data TEXT)''')
    con.commit()

    def __init__(self):
        print("Initialised Game Container")

    #Adds game to SQL database
    def addGame(self, gameID, gameType, data='NULL'):
        self.cursor.execute(f'''INSERT INTO games VALUES(\"{gameID}\",{gameType.value},\'{data}\');''')
        self.con.commit()
        return

    #gets game from ID
    def grabGame(self, gameID):
        self.cursor.execute(f'''SELECT * FROM games WHERE gameID = "{gameID}"''')
        return self.cursor.fetchone()

    #update data in game
    def updateGame(self, gameID, data):
        self.cursor.execute(f'''UPDATE games SET data = \'{data}\' WHERE gameID = "{gameID}"''')
        self.con.commit()
        return

Container = GamesContainer()

class Play(commands.Cog):


    def __init__(self,bot: commands.Bot):
        print("Initialising Play Command Cog")
        #prepare bot reference and account manager module
        self.bot: commands.Bot = bot
        self.Manager = AccountManager()

        #load individual game modules to objects
        self.tictactoe = Tictactoe(Container, bot, self.Manager)
        print("Initialised Play Command Cog")

    #Reaction listener, checks for reactions
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.bot.user.id:
            record = Container.grabGame(payload.message_id)
            if record is not None:
                game = record[1]

            #check game against gametype value
            if game == Games.TicTacToe.value:
                await self.tictactoe.updateGame(payload, record)

    #command definitions
    @commands.hybrid_command(name="tictactoe",aliases=["ttt","nc"])
    @app_commands.describe(player2="Enter the id of the second player")
    async def tictactoe(self, ctx: commands.Context, player2: discord.Member = None):
        await self.tictactoe.createGame(ctx, player2)

    @commands.command(name="ConnectFour",aliases=["c4","connect"])
    async def connectfour(self, ctx):
        await ctx.send("WIP!")
    
async def setup(bot):
    await bot.add_cog(Play(bot))

