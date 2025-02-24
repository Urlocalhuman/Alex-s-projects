import sys
import os
import threading
from pystyle import Colors, Colorate
from rich.console import Console

red = Colors.red
yellow = Colors.yellow
threadrunning = False

# HOME VERSION OF THE PROJECT I STARTED AT SCHOOL

# list of planned statements:
# if <arguments>
# end - tells interpreter where an if/loop/else ends
# else
# log <logtype> <log>
# logset <options> - sets up the logger (should always be the first line of code)
# var <data> - declares a variable and sets its value to <data>
# op <saveto> <operation> - performs an operation and saves it to <saveto>
# engine <config> - sets up the rendering engine as either: console, tkinter or pygame (should always be second line of code)
# render <objtype> <data> - renders an object which can be text or shape or image (with console renderer only text, tkinter will have image and text and pygame will have all)
# logstart/logstop - starts or stops the logging thread
# 
# important things for interpreter:
# varstorage: dict that stores all of the variables
# renderlist: list that stores all of the objects that will be rendered 
# rendertype: can be 'c', 't' and 'p' (console, tkinter, pygame) 
#
# modes:
# normal or -i: interprets file
# -c: attempts to compile file into python
# 
# datatype declaration:
# int - number
# float - number
# string - " stringdata " (requires space between quotation marks and data)

console = Console()

def merge(s):
    m = ""
    for i in range(len(s)):
        m = m + " " + s[i]
    return m.strip()

def xprint(color, text):
    print(Colorate.Color(color, text))

class Interpreter:
    def __init__(self, script):
        self.script = script
        self.varstorage = {"blankvar": 0}
        self.renderlist = []
        self.rendertype = "c"
        self.logger = 0
        self.logger_exists = False
        self.stopcode = 0
        self.logthread = 0

    def close(self, line=0):
        global threadrunning
        if self.logger_exists:
            threadrunning = False
            try:
                self.logthread.join()
            except:
                pass
            self.logger.stop()
        
        if self.stopcode == 0:
            xprint(yellow, "Script ended with exit code 0")
        elif self.stopcode == 1:
            xprint(red, f"Script terminated due to error: log already is set up! (line {line})")
        elif self.stopcode == 2:
            xprint(red, f"Script terminated due to error: log setup missing arguments! (line {line})")
        exit()
            

    def start(self):
        global threadrunning
        for i in range(len(self.script)):
            if self.script[i][0] == "logset":
                if len(self.script[i]) >= 2:
                    if self.logger_exists == False:
                        threadrunning = True
                        self.logger_exists = True
                        self.logger = Logger(merge(self.script[i][1:]))
                        self.logthread = threading.Thread(target=self.logger.start)
                    else:
                        self.stopcode = 1
                        self.close(line=i+1)
            else:
                self.stopcode = 2
                self.close(line=i+1)               


class Logger:
    def __init__(self, location):
        self.log = [["Info", "Log started"]]
        if not os.path.exists(location):
            self.location = os.getcwd()
            self.log.append(["Warn", "Location does not exist, using default"])
        else:
            self.location = location

    def addlog(self, entry):
        self.log.append(entry)

    def start(self):
        global threadrunning
        updtimer = 3000
        if os.path.isfile(f"{self.location}\\log.txt"):
            os.remove(f"{self.location}\\log.txt")
        open(f"{self.location}\\log.txt", "x").close()
        while True:
            if not threadrunning:
                break
            if updtimer == 3000:
                updtimer = 0
                log = ""
                for i in range(len(self.log)):
                    log = log + """
                    """ + f"{self.log[i][0]}: {self.log[i][1]}"
                with open(f"{self.location}\\log.txt", "w") as file:
                    file.write(log)

    def stop(self):
        log = ""
        for i in range(len(self.log)):
            log = log + """
            """ + f"{self.log[i][0]}: {self.log[i][1]}"
        with open(f"{self.location}\\log.txt", "w") as file:
            file.write(log)       


                    



class Compiler:
    def __init__(self, script):
        print("not working on this yet")
        self.script = script
    def start(self):
        pass


if len(sys.argv) <= 1:
    print("Not enough arguments given!")
    quit()

with open(f"{sys.argv[2 if len(sys.argv) == 3 else 1]}", "r") as file:
    script = file.readlines()
    script2 = []
    for i in range(len(script)):
        script2.append(script[i].split())
    script = script2

if len(sys.argv) == 3:
    if sys.argv[1] == "-c":
        c = Compiler(script)
        c.start()
    elif sys.argv[1] == "-i":
        main = Interpreter(script)
        main.start()
else:
    main = Interpreter(script)
    main.start()
