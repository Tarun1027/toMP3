#!/usr/bin/python

# Griffin Saiia, ffmpeg wrapper to convert all common audio types to .mp3

import os
import sys
import subprocess
from Tkinter import *

# struct to store file data neatly
class fileData:
    def __init__(self):
        self.name = ""
        self.path = ""
        self.ext = ""

class GUI(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        ents = self.makeform()
        self.bind('<Return>', (lambda event, e=ents: self.fetch(e)))
        b1 = Button(root, text="Run", command=(lambda e=ents: self.fetch(e)))
        b1.pack(side=LEFT, padx=5, pady=5)
        b2 = Button(root, text="Quit", command=root.quit)
        b2.pack(side=RIGHT, padx=5, pady=5)

    def updateGUI(self):
        root.update_idletasks()

    def fetch(self, entries):
        entries[2].configure(text="Running...")
        choice = entries[0].get()
        path = entries[1].get()
        entries[0].delete(0, END)
        entries[1].delete(0, END)
        self.updateGUI()
        run(choice, path, entries)
        entries[3].configure(text="    ...Done.")

    def makeform(self):
        root.title(".mp3 Converter")
        title = Label(root, text="Griffin\'s to .mp3 Converter")
        title.pack(side=TOP, padx=15, pady=15)
        acknowledge = Label(root, text = "Special thanks to the genius' who developed ffmpeg")
        acknowledge.pack(padx=5)
        border = Label(root, text="----------------------------------------------------------------------------")
        border.pack(pady=5)
        entries = []
        params = ["single or batch?", "/path/to/your/file_or_directory"]
        for param in params:
            row = Frame(root)
            lab = Label(row, width=30, text=param, anchor='w')
            ent = Entry(row)
            row.pack(side=TOP, fill=X, padx=20, pady=20)
            lab.pack(side=LEFT)
            ent.pack(side=RIGHT, expand=YES, fill=X)
            entries.append(ent)
        warning = Label(root, text = "**Note: ffmpeg doesn't support spaces in file names.")
        warning.pack(padx=5)
        border3 = Label(root, text="----------------------------------------------------------------------------")
        border3.pack(pady=5)
        process = Label(root)
        process.pack()
        entries.append(process)
        output = Label(root)
        output.pack()
        entries.append(output)
        border2 = Label(root, text="----------------------------------------------------------------------------")
        border2.pack(pady=5)
        return entries


# dictionary to store ffmpeg commands
def flac():
    command = []
    command.append("ffmpeg -i ")
    command.append(" -ab 320k -map_metadata 0 -id3v2_version 3 ")
    command.append(".mp3 >/dev/null 2>&1")
    return command

def m4a():
    command = []
    command.append("ffmpeg -i ")
    command.append(" -acodec libmp3lame -ab 128k -map_metadata 0 ")
    command.append(".mp3 >/dev/null 2>&1")
    return command

def m4b():
    command = []
    command.append("ffmpeg -i ")
    command.append(" -acodec libmp3lame -ar 22050 ")
    command.append(".mp3 >/dev/null 2>&1")
    return command

def wav():
    command = []
    command.append("ffmpeg -i ")
    command.append(" -vn -ar 44100 -ac 2 -ab 192k -map_metadata 0 -f mp3 ")
    command.append(".mp3 >/dev/null 2>&1")
    return command

def wma():
    command = []
    command.append("ffmpeg -i ")
    command.append(" -acodec libmp3lame -ab 192k -map_metadata 0 ")
    command.append(".mp3 >/dev/null 2>&1")
    return command

def alac():
    command = []
    command.append("ffmpeg -i ")
    command.append(" -ac 2 -f wav -map_metadata 0 - | lame -V 2 -")
    command.append(".mp3 >/dev/null 2>&1")
    return command

def aiff():
    command = []
    command.append("ffmpeg -i ")
    command.append(" -f mp3 -acodec libmp3lame -ab 192000 -ar 44100 -map_metadata 0 ")
    command.append(".mp3 >/dev/null 2>&1")
    return command

commands = {"flac": flac,
            "m4a": m4a,
            "m4b": m4b,
            "wav": wav,
            "wma": wma,
            "caf": alac,
            "aif": aiff
}

def run(line, path, entries):
    try:
        fileArray = []
        if(line == "single" or line == "Single"):
            fileD = fileData()
            extractData(fileD, path)
            fileArray.append(fileD)
        else:
            fileArray = scanDir(path, fileArray)
        convert(fileArray, entries)
    except IndexError:
        line = "batch"
        run(line, path, entries)
    except OSError:
        entries[3].configure(text="     ...Error locating file(s)")

def scanDir(directory, fileArray):
    for file in os.listdir(directory):
        split = file.split(".")
        try:
            commands[split[1]]
            fileD = fileData()
            fileD.path = directory
            fileD.name = split[0]
            fileD.ext = split[1]
            fileArray.append(fileD)
        except:
            print("bad file -- "+file)
    return fileArray

def convert(fileArray, entries):
    try:
        for fileD in fileArray:
            input = fileD.path+fileD.name+"."+fileD.ext
            output = fileD.path+fileD.name
            commandFrame = commands[fileD.ext]()
            command = commandFrame[0]+input+commandFrame[1]+output+commandFrame[2]
            subprocess.check_output(command, shell=True)
    except subprocess.CalledProcessError:
        entries[3].configure(text="Error converting "+fileD.name+"."+fileD.ext)
    except KeyError:
        entries[3].configure(text="Error not a supported file format.")

def extractData(fileD, raw):
    firstsplit = raw.split("/")
    i = 0
    while(i < (len(firstsplit) - 1)):
        if(i == 0):
            fileD.path = firstsplit[i] + "/"
        else:
            fileD.path = fileD.path + firstsplit[i] + "/"
        i += 1
    secondsplit = firstsplit[(len(firstsplit)-1)].split(".")
    fileD.name = secondsplit[0]
    fileD.ext = secondsplit[1]


#Execute the application
if __name__ == "__main__":
        root = Tk()
        gui =  GUI(root)
        root.mainloop()
