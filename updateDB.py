import sqlite3
import json

#Used to update the data column in every record of the accounts db
#Not very easy to read but is only needed for development purposes


connection = sqlite3.connect("./accounts.db")
cursor = connection.cursor()
db = cursor.execute("SELECT accountid, data FROM accounts").fetchall()
print(db)
for acc in db:
    print(acc)
    accDat = json.loads(acc[1])
    print(accDat)
    datNew = {"tttwins":accDat["tttwins"],"tttdraws":accDat["tttdraws"],"tttlosses":accDat["tttlosses"],"c4wins":accDat["c4wins"],"c4draws":accDat["c4draws"],"c4losses":accDat["c4losses"]}
    print(datNew)
    cursor.execute(f'''UPDATE accounts SET data='{json.dumps(datNew)}' WHERE accountID={acc[0]}''')
connection.commit()