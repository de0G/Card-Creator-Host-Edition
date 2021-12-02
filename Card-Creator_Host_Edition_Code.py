import tkinter as tk
from tkinter import font
from tkinter.messagebox import showerror, askquestion, showinfo
import os
from cryptography.fernet import Fernet
from datetime import datetime
import pyperclip
import random

def ProcessGame():
    game = nameEntry.get().strip()

    illegal = ["(", ")", "[", "]", ":", " ", "{", "}", "\\", "/", "."]

    valid = True

    for criminal in illegal:
        if criminal in game:
            valid = False

    if game == "":
        showerror("ERROR: Can't Process Game","You must enter the name of the game")
    elif not valid:
        showerror("ERROR: Can't Process Game","Deck name has an illegal character (e.g. spaces, colons, slashes, etc.)\n\nTry replacing spaces with underscores")
    elif not os.path.isdir(os.path.join(gamesDirectory, game)):
        showerror("ERROR: Can't Process Game",f"There is no folder in the 'Games' directory called '{game}'!\n\nCreate this folder and put the desired decks there")
    else:
        directory = os.path.join(gamesDirectory, game)
        gameFile = open(f"{directory}\\{game.upper()}.deck", "w")
        metaFile = open(f"{directory}\\META.data", "w")

        gameList = []

        whiteCount = 0
        blackCount = 0
        totalCount = 0
        date = datetime.now().strftime("%d/%m/%y %H:%M:%S")
        
        for deckName in os.listdir(directory):
            if deckName.endswith(".txt"):
                if ValidDeck(deckName, directory):
                    deckPath = os.path.join(directory, deckName)
                    deck = open(deckPath, "r")
                    decrypt(deckPath)

                    for card in deck:
                        if card != "":
                            if "_" in card:
                                blackCount += 1
                            else:
                                whiteCount += 1

                            totalCount += 1
                            gameList.append(card)

                    encrypt(deckPath)

        for i in range(0, len(gameList)):
            addition = random.choice(gameList)
            gameFile.write(addition)
            
            gameList.remove(addition)

        metaFile.write(f"{whiteCount}_{blackCount}_{totalCount}_{date}")

        metaFile.close()
        gameFile.close()
        
        encrypt(f"{directory}\\{game.upper()}.deck")
        
        showinfo("Processing Successful!", f"The game '{game}' has successfully been processed!\n\nPress 'Copy to Clipboard' for the game to be copied")
                    
def DisplayInfo():
    game = nameEntry.get().strip()

    directory = os.path.join(gamesDirectory, game)
    metaLocation = f"{directory}\\META.data"

    if not os.path.isdir(directory):
        showerror("ERROR: Can't Display Game",f"There is no folder in the 'Games' directory called '{game}'!\n\nCreate this folder and put the desired decks there")
    elif not os.path.isfile(metaLocation):
        showerror("ERROR: Can't Display Game Information","You must process the game first!")
    else:
        metaFile = open(metaLocation, "r")

        rawData = metaFile.read()
        dataList = rawData.split("_")

        metaFile.close()

        data = f"""
White Cards: {dataList[0]}
Black Cards: {dataList[1]}
Total Cards: {dataList[2]}

Processing Date: {dataList[3]}"""

        showinfo(f"{game} Information", f"Information for the '{game}' game:\n{data}")

def Clipboard():
    game = nameEntry.get().strip()

    directory = os.path.join(gamesDirectory, game)
    gameLocation = f"{directory}\\{game.upper()}.deck"

    if not os.path.isdir(directory):
        showerror("ERROR: Can't Copy to Clipboard",f"There is no folder in the 'Games' directory called '{game}'!\n\nCreate this folder and put the desired decks there")
    elif not os.path.isfile(gameLocation):
        showerror("ERROR: Can't Copy to Clipboard","You must process the game first!")
    else:
        decrypt(gameLocation)
        gameFile = open(gameLocation, "r")

        gameData = gameFile.read().strip()

        pyperclip.copy(gameData)

        gameFile.close()
        encrypt(gameLocation)

        showinfo("Copied to Clipboard", f"Copied to Clipboard")

def GetCache():
    path = os.path.join(dataDirectory, "cache.txt")
    cache = open(path, "r")
    lastFile = cache.read()

    return lastFile

def ValidDeck(deck, directory):
    deck = open(os.path.join(directory, deck), "r")
    valid = True

    text = deck.read()
    if "\n" in text:
        valid = False
    elif text.strip() == "":
        valid = False
        
    return valid

def encrypt(file):
    keyFile = open(os.path.join(dataDirectory, "key.key"), "rb")
    key = keyFile.read()
    key = key[:-1]
    keyFile.close()

    with open(file, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(file, 'wb') as f:
        f.write(encrypted)

    log(f"'{file}' AUTOMATICALLY ENCRYPTED")

def decrypt(file):
    keyFile = open(os.path.join(dataDirectory, "key.key"), "rb")
    key = keyFile.read()
    key = key[:-1]
    keyFile.close()
    
    f = open(file, 'rb')
    data = f.read()
    f.close()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)

    f = open(file, 'wb')
    f.write(decrypted)
    f.close()

    log(f"'{file}' AUTOMATICALLY DECRYPTED")

def log(message):
    logFile = open(os.path.join(dataDirectory, "log.txt"), "a+")
    logTime = datetime.now().strftime("[%d/%m/%y %H:%M:%S]")
    logFile.write(f"{logTime} {message}\n")
    logFile.close()

version = "1.0"
dataDirectory = f"{os.getcwd()}\\program_files"
gamesDirectory = f"{os.getcwd()}\\Games"

root = tk.Tk()
root.title(f"deOG's Card-Creator {version}")
root.iconbitmap(os.path.join(dataDirectory, "logo.ico"))

cardColours = ["white","black"]
decider = 0

backgroundColour = "black"
textColour = "white"

w_height = 240
w_width = 600

normalFont = ("Calibri", 20)
inputFont = ("Calibri", 13)
buttonFont = ("Calibri", 14)

canvas = tk.Canvas(root, height=w_height, width=w_width)
canvas.pack()

titleLabel = tk.Label(root, text = "The Card-Creator", font = ("Trebuchet MS", 30))
titleLabel.place(anchor = "n", relx = 0.56, rely = 0.04, relheight = 0.3, relwidth = 0.6)

versionLabel = tk.Label(root, text = "[Host Edition]", font = ("Trebuchet MS", 13))
versionLabel.place(anchor = "n", relx = 0.56, rely = 0.26, relheight = 0.15, relwidth = 0.6)

humanityLogo = tk.PhotoImage(file = os.path.join(dataDirectory, "humanityLogo.png")).subsample(3,3)
humanityLabel = tk.Label(root, image = humanityLogo)
humanityLabel.place(anchor = "n", relx = 0.22, rely = 0.08, relheight = 0.28, relwidth = 0.15)

nameEntry = tk.Entry(root, font = inputFont, cursor = "xterm", bd = 2, justify = "center")
nameEntry.place(anchor = "n", relx = 0.5, rely = 0.45, relwidth = 0.9, relheight = 0.17)

nameEntry.insert(0, GetCache())

#https://anzeljg.github.io/rin2/book2/2405/docs/tkinter/cursors.html - Shows all mouse cursor options with images

processButton = tk.Button(root, text = "Process Game", font = buttonFont, command=lambda:ProcessGame())
processButton.place(relx = 0.22, rely = 0.68, relheight = 0.2, relwidth = 0.25, anchor = "n")

infoButton = tk.Button(root, text = "Game Info", font = buttonFont, command=lambda:DisplayInfo())
infoButton.place(relx = 0.5, rely = 0.68, relheight = 0.2, relwidth = 0.25, anchor = "n")

copyButton = tk.Button(root, text = "Copy To Clipboard", font = buttonFont, command=lambda:Clipboard())
copyButton.place(relx = 0.78, rely = 0.68, relheight = 0.2, relwidth = 0.25, anchor = "n")

versionLabel = tk.Label(root, text = f"Version: {version}", font = ("Calibri", 13))
versionLabel.place(anchor = "n", relx = 0.5, rely = 0.91, relheight = 0.06, relwidth = 0.23)

root.mainloop()
