#All code relating to the account management and related Cog
import string
import discord
from discord.ext import commands
from discord import app_commands
import sqlite3
import json

class AccountManager:

    def __init__(self):
        self.con = sqlite3.connect("./accounts.db")
        self.cursor = self.con.cursor()

        #Discord Member ID; Number of coins; VIP Status (0 or 1); All other data
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS accounts(accountID INTEGER PRIMARY KEY, coins INTEGER, vip INTEGER, data STRING)''')
        self.con.commit()
        print("Initialised account manager")
    
    def checkAccount(self, accountID):
        self.cursor.execute(f'''SELECT * FROM accounts WHERE accountID = {accountID}''')
        account = self.cursor.fetchone()
        print(accountID)
        if account is None:
            data = {"tttwins":0,"c4wins":0}
            data = json.dumps(data)
            self.cursor.execute(f'''INSERT INTO accounts VALUES({accountID},0,0,'{data}')''')
            self.con.commit()

    def getAccount(self, accountID):
        self.cursor.execute(f'''SELECT * FROM accounts WHERE accountID = {accountID}''')
        data = self.cursor.fetchone()
        if data is None:
            self.checkAccount(accountID)
            return [accountID,0,0,{"tttwins":0,"c4wins":0}]
        else:
            return data

    def updateAccountCoins(self, accountID, quantity: int = 0):
        self.cursor.execute(f'''SELECT * FROM accounts WHERE accountID = {accountID}''')
        coins = self.cursor.fetchone()[1]
        self.cursor.execute(f'''UPDATE accounts SET coins = {coins + quantity} WHERE accountID = {accountID}''')
        self.con.commit()
        return
    
    def updateAccountData(self, accountID, data):
        self.cursor.execute(f'''UPDATE accounts SET data='{data}' WHERE accountID={accountID}''')
        self.con.commit()
        return
    def resetAccount(self, accountID):
        pass

class Account(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.Manager = AccountManager()
    
    @commands.hybrid_command(name="coins", alias=["balance","bal"])
    @app_commands.describe(member="The person you wish to see the balance of")
    async def coins(self, ctx: commands.Context, member: str = None):
        if member is None:
            account = self.Manager.getAccount(ctx.author.id)
            await ctx.send(f"You have {account[1]} coins!")
        else:
            return

async def setup(bot):
    await bot.add_cog(Account(bot))