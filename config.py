import json
import os

try:

    #settings configuration
    token = ""
    while len(token) < 5:
        token = input("Enter the Bot Token: ")
        if len(token) < 5:
            print("Bot token is required for the bot to work")

    #make directory for the file
    try:
        print("Making config folder")
        os.mkdir("config")
    except FileExistsError:
        print("Folder already exists, continuing")
    except all:
        print("An error has occcured, please try again later.")
        os.__exit()
    
    #prepare dictionary for file config
    config = {"TOKEN":token}
    #prepare JSON to write to file (chosen over json.dump for user friendliness)
    formatJson = json.dumps(config, indent=4)
    try:
        with open("config/cfg.json", "w+") as file:
            print("Attempting to write config file \"config/cfg.json\"")
            file.write(formatJson)
            file.close()
        print("File written successfully")
    except all:
        print("An error has occurred")
        os.__exit()

except KeyboardInterrupt:
    print("Keyboard Interrupt - Ending config")