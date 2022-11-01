import discord
import json
from codecs import ignore_errors
import random
from .enums import Games

class Tictactoe:
    def __init__(self, container, bot, accountmanager):
        self.Container = container
        self.bot = bot
        self.Manager = accountmanager
        print("Initialised TicTacToe game module")

    #manually update TTT Grid Embed
    async def TTT_updateGrid(self, grid, msg):
        #Grab Discord Embed for editing
        embedVar = msg.embeds[0]
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
    def checkWin(self, grid, player):
        if player == 1:
            notPlayer = 2
        else:
            notPlayer = 1
        
        #check rows
        for row in grid:
            if row == [player, player, player]:
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
        diagOne = str(grid[0][0]) + str(grid[1][1]) + str(grid[2][2])
        if diagOne == str(player) * 3:
            return True
        diagTwo = str(grid[0][2]) + str(grid[1][1]) + str(grid[2][0])
        if diagTwo == str(player) * 3:
            return True
        
        #if checks fail, no win
        return False

    async def updateGame(self, payload, record):
        data = json.loads(record[2])
        #if game ended, don't bother doing anything else
        if data["turn"] == 3:
            return
        
        msg = payload.message_id
        chnl = await self.bot.fetch_channel(payload.channel_id)
        msg = await chnl.fetch_message(msg)

        emojis = [['1️⃣','2️⃣','3️⃣'],['4️⃣','5️⃣','6️⃣'],['7️⃣','8️⃣','9️⃣']]
       
        grid = data["grid"]

        #NOTE For all Turn=4 and Update Game statements; Used to ensure game can't be modified in multiple processes at once, as it breaks the game
        if data["turn"] == 0:
            data["turn"] = 4
            self.Container.updateGame(payload.message_id, json.dumps(data))

            if data["playerOne"] == payload.member.id:
                for x in range(3):
                    try:
                        pos = emojis[x].index(payload.emoji.name)
                        if grid[x][pos] == 0:
                            grid[x][pos] = 1
                            data["turn"] = 1
                            break
                        else:
                            data["turn"] = 0
                    except ValueError:
                        ignore_errors
                if self.checkWin(grid, 1) == True:
                    data["turn"] = 3
                    data["winner"] = payload.member.id 
                    self.Manager.updateAccountCoins(payload.member.id, 150)     
                    account = self.Manager.getAccount(payload.member.id)
                    accData = json.loads(account[3])
                    accData["tttwins"] += 1
                    self.Manager.updateAccountData(payload.member.id, json.dumps(accData))
                else:
                    await self.TTT_updateGrid(grid, msg)
                    

        elif data["turn"] == 1 and data["playerTwo"] != 0:
            data["turn"] = 4
            self.Container.updateGame(payload.message_id, json.dumps(data))
            if data["playerTwo"] == payload.member.id:
                for x in range(3):
                    try:
                        pos = emojis[x].index(payload.emoji.name)
                        if grid[x][pos] == 0:
                            grid[x][pos] = 2
                            data["turn"] = 0
                            break
                        else:
                            data["turn"] = 0
                    except ValueError:
                        ignore_errors
                if self.checkWin(grid, 2) == True:
                    data["turn"] = 3
                    data["winner"] = payload.member.id
                    self.Manager.updateAccountCoins(payload.member.id, 150)
                    account = self.Manager.getAccount(payload.member.id)     
                    accData = json.loads(account[3])
                    accData["tttwins"] += 1
                    self.Manager.updateAccountData(payload.member.id, json.dumps(accData))
                else:
                    await self.TTT_updateGrid(grid, msg)
                    
        #If bot's turn generate random position
        if data["turn"] == 1 and data["playerTwo"] == 0:

            data["turn"] = 4
            self.Container.updateGame(payload.message_id, json.dumps(data))

            #check for open spaces
            open = False
            for row in grid:
                if 0 in row:
                    open = True

            moveMade = False
            tmpGrid = [[],[],[]]
            for i in range(3):
                for j in range(3):
                    tmpGrid[i].append(grid[i][j])
 
            #check for winning places
            for x in range(3):
                for y in range(3):
                    
                    if tmpGrid[x][y] == 0:
                        tmpGrid[x][y] = 2
                        if self.checkWin(tmpGrid, 2) and not moveMade: 
                            moveMade = True
                            movX = x
                            movY = y
                        tmpGrid[x][y] = 0
                        
            for x in range(3):
                for y in range(3):                    
                    if tmpGrid[x][y] == 0:
                        tmpGrid[x][y] = 1
                        if self.checkWin(tmpGrid, 1) and not moveMade: 
                            moveMade = True
                            movX = x
                            movY = y
                        tmpGrid[x][y] = 0

            if grid[1][1] == 0 and not moveMade:
                moveMade = True
                movX = 1
                movY = 1
            #random move until valid one taken
            while open and not moveMade:
                movX = random.randint(0,2)
                movY = random.randint(0,2)
                if grid[movX][movY] == 0:
                    moveMade = True
            if open:
                grid[movX][movY] = 2

            data["turn"] = 0
            if self.checkWin(grid, 2) == True:
                    data["turn"] = 3
                    data["winner"] = 0
            else:
                    await self.TTT_updateGrid(grid, msg)


        draw = 1
        for row in grid:
            if 0 in row:
                draw = 0
        if draw == 1 and data["turn"] != 3:
            data["turn"] = 3
            data["winner"] = 1

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
        self.Container.updateGame(payload.message_id, json.dumps(data))

    async def createGame(self, ctx, player2):
        
        if type(ctx.interaction) != type(None):
            await ctx.interaction.response.send_message(f"{ctx.author.mention} ran TicTacToe")
        else:
            await ctx.send(f"{ctx.author.mention} ran TicTacToe")
        self.Manager.checkAccount(ctx.author.id)
        #format player 2 ID (Removes <@>)
        if player2 == None:
            player2 = "0"
        elif type(player2) == discord.Member:
            player2 = player2.id
        elif len(player2) > 1 and '@' in player2:
            player2 = int(player2[2:-1])
            self.Manager.checkAccount(ctx.author.id)
        if int(player2) == self.bot.user.id:
            player2 = 0
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
        dat = {"grid":grid, "playerOne":ctx.author.id,"playerTwo":int(player2),"turn":0, "winner":""}
        self.Container.addGame(gameID=id.id, gameType=Games.TicTacToe, data=json.dumps(dat))