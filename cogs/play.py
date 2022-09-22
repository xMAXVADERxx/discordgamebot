from codecs import ignore_errors
from re import X
import discord
from discord.ext import commands
import sqlite3
import enum
import json
import math
import random
#handles the storing and management of games
class GamesContainer:
    
    #init sqlite
    con = sqlite3.connect("games.db")
    cursor = con.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS games(gameID TEXT PRIMARY KEY, gameType INTEGER, data TEXT)''')
    con.commit()

    def __init__(self):
        print("Initialised Container")

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

class Games(enum.Enum):
    TicTacToe = 1

class Play(commands.Cog):
    
    
    def __init__(self,bot):
        self.bot = bot

    #manually update TTT Grid Embed
    async def TTT_updateGrid(self, grid, msg):
        embedVar = msg.embeds[0]
        newMsg = msg
        txt = ""
        for row in grid:
            for column in row:
                if column == 0:
                    txt += ":white_large_square:"
                elif column == 1:
                    txt += ":white_check_mark:"
                elif column == 2:
                    txt += ":negative_squared_cross_mark:"
            txt += '\n'
        embedVar.description = txt

        await msg.edit(embed=embedVar)
        return

    #check win condition
    def TTT_checkWin(self, grid, player):
        if player == 1:
            notPlayer = 2
        else:
            notPlayer = 1
        
        #check rows
        for row in grid:
            if 0 not in row and notPlayer not in row:
                return True
        
        #check columns
        for x in range(3):
            cnt = 0
            for row in grid:
                if row[x] == player:
                    cnt += 1
            if cnt == 3:
                return True
        
        #check diagonals
        cnt = 0
        cntNeg = 0
        for x in range(3):
            if grid[x][x] == player:
                cnt += 1
            if grid[x][2-x] == player:
                cntNeg += 1
        if cnt == 3 or cntNeg == 3:
            return True
        
        #if checks fail, no win
        return False

    async def checkTTT(self, payload, record):
        data = json.loads(record[2])
        #if game ended, don't bother doing anything else
        if data["turn"] == 3:
            return
        
        msg = payload.message_id
        chnl = await self.bot.fetch_channel(payload.channel_id)
        msg = await chnl.fetch_message(msg)

        emojis = [['1️⃣','2️⃣','3️⃣'],['4️⃣','5️⃣','6️⃣'],['7️⃣','8️⃣','9️⃣']]
       
        grid = data["grid"]

        if data["turn"] == 0:
            data["grid"] = 4
            Container.updateGame(payload.message_id, json.dumps(data))

            if data["playerOne"] == payload.member.id:
                for x in range(3):
                    try:
                        if grid[x][emojis[x].index(payload.emoji.name)] == 0:
                            grid[x][emojis[x].index(payload.emoji.name)] = 1
                            data["turn"] = 1
                            #hideous
                            await self.TTT_updateGrid(grid, msg)
                            break
                    except ValueError:
                        ignore_errors
                if self.TTT_checkWin(grid, 1) == True:
                    data["turn"] = 3
                    data["winner"] = payload.member.id      

        elif data["turn"] == 1:
            data["grid"] = 4
            Container.updateGame(payload.message_id, json.dumps(data))
            if data["playerTwo"] == payload.member.id:
                for x in range(3):
                    try:
                        if grid[x][emojis[x].index(payload.emoji.name)] == 0:
                            grid[x][emojis[x].index(payload.emoji.name)] = 2
                            data["turn"] = 0
                            await self.TTT_updateGrid(grid,msg)
                            break
                    except ValueError:
                        ignore_errors
                if self.TTT_checkWin(grid, 2) == True:
                    data["turn"] = 3
                    data["winner"] = payload.member.id
                    
            
        #If bot's turn generate random position
        if data["turn"] == 1 and data["playerTwo"] == "0":

            #check for open spaces
            valid = True
            for row in grid:
                if 0 in row:
                    valid = False

            #random move until valid one taken
            while valid == False:
                x = random.randint(0,2)
                y = random.randint(0,2)
                if grid[x][y] == 0:
                    valid = True
                    
            grid[x][y] = 2
            data["turn"] = 0
            if self.TTT_checkWin(grid, 2) == True:
                    data["turn"] = 3
                    data["winner"] = 0


        draw = 1
        for row in grid:
            if 0 in row:
                draw = 0
        if draw == 1:
            data["turn"] = 3
            data["winner"] = 1

        await self.TTT_updateGrid(grid, msg)

        #check if there is a winner, update message accordingly
        if data["turn"] == 3:
            embedVar = msg.embeds[0]
            newMsg = msg
            txt = ""
            for row in grid:
                for column in row:
                    if column == 0:
                        txt += ":white_large_square:"
                    elif column == 1:
                        txt += ":white_check_mark:"
                    elif column == 2:
                        txt += ":negative_squared_cross_mark:"
                txt += '\n'
        
            if data["winner"] == 0:
                winner = "Computer"
            elif data["winner"] == 1:
                winner = "Draw"
            else:
                winner = f'<@{data["winner"]}>'

            txt += f"Winner: {winner}"

            embedVar.description = txt

            await msg.edit(embed=embedVar)

        data["grid"] = grid
        Container.updateGame(payload.message_id, json.dumps(data))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.id != self.bot.user.id:
            chnl = await self.bot.fetch_channel(payload.channel_id)
            record = Container.grabGame(payload.message_id)
            game = record[1]

            #check game against gametype value
            if game == Games.TicTacToe.value:
                await self.checkTTT(payload, record)

    


    @commands.command(name="tictactoe",aliases=["ttt","nc"])
    async def tictactoe(self, ctx, player2="0"):
        #format player 2 ID to fix other code
        if len(player2) > 1:
            player2 = int(player2[2:-1])
        grid = [[0,0,0],[0,0,0],[0,0,0]]
        msg = ""
        for x in range(3):
            for y in range(3):
                msg += ':white_large_square:'
            msg += '\n'
        embedVar = discord.Embed(title="TicTacToe", description=f"{msg}")
        id = await ctx.channel.send(embed=embedVar)
        reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']
        for emoji in reactions:
            await id.add_reaction(emoji)
        #make data dict in format {grid, creator, player2, gameState (Used as turn counter [0-1] and game finished flag [2])}
        dat = {"grid":grid, "playerOne":ctx.author.id,"playerTwo":player2,"turn":0, "winner":""}
        Container.addGame(gameID=id.id, gameType=Games.TicTacToe, data=json.dumps(dat))

    @commands.command(name="ConnectFour",aliases=["c4","connect"])
    async def connectfour(self, ctx):
        await ctx.send("WIP!")
        
    
def setup(bot):
    bot.add_cog(Play(bot))

