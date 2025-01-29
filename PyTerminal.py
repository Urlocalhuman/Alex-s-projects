from pystyle import Colors, Colorate
from rich.console import Console
import os
import msvcrt

red = Colors.red
green = Colors.green
yellow = Colors.yellow
blue = Colors.blue
lblue = Colors.light_blue
lgray = Colors.light_gray
c = "c"
currentcol = lgray
devmode = False

console = Console()


# Print with colors
def print_colored(text, color=Colors.white):
    print(Colorate.Color(color, text))

def print_gradient(text, colour=Colors.red_to_blue):
    gradient = Colorate.Horizontal(colour, text)
    print(gradient)

# Wait for a keypress and return the pressed key
def wait_for_keypress():
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch().decode('utf-8')
            return key

def slashcheck(s=""):
    if not s.endswith("\\"):
        s += "\\"
    return s

def getpath(cmd):
    p = ""
    for i in range(len(cmd)):
        p = p + " " + cmd[i]
    p = p.strip()
    p = slashcheck(p)
    if os.path.exists(p):
        return [True, p] 
    else:
        p = ""
        for i in range(len(cmd)):
            p = p + cmd[i]
        p = p.strip()
        p = slashcheck(p)
        if os.path.exists(p):        
            return [True, p]
        else:
            return [False, p]



def xprint(string, colour="None", mode="n"):
    if mode == "n":
        print(string)
    elif mode == "c":
        if colour == "None":
            print_colored(string, Colors.green)
        else:
            print_colored(string, colour)
    elif mode == "g":
        if colour == "None":
            print_gradient(string, Colors.green_to_yellow)
        else:
            print_gradient(string, colour)

cmd = []
cd = "C:\\"
while True:
    cmd = (input(Colorate.Color(currentcol, f"{cd}>> ")).strip()).split()
    if len(cmd) <= 1:
        continue
    if cmd[0] == "cd" and len(cmd) >= 2:
        returnvalue = getpath(cmd[1:])
        if returnvalue[0]:
            cd = returnvalue[1]
        else:
            cmd.insert(1, cd)
            if getpath(cmd[1:])[0]:
                cd = cd + returnvalue[1]
            else:        
                xprint(f"Path does not exist: {returnvalue[1]}", red, c)
        returnvalue = None

    elif cmd[0] == "mkfile" and len(cmd) >= 2:
        try:
            with open(cd + cmd[1], "x"):
                xprint(f"File {cd + cmd[1]} created", green, c)
        except Exception as e:
            xprint(f"Error creating {cd + cmd[1]} {e}", red, c)

    elif cmd[0] == "mkdir" and len(cmd) >= 2:
        try:
            os.mkdir(cd + cmd[1])
            xprint(f"Directory {cd + cmd[1]} created", green, c)
        except Exception as e:
            xprint(f"Error creating directory {cd + cmd[1]} {e}", red, c)

    elif cmd[0] == "del" and len(cmd) >= 2:
        try:
            os.remove(cd + cmd[1])
            xprint(f"Removed {cd + cmd[1]}", green, c)
        except Exception as e:
            xprint(f"Error deleting {cd + cmd[1]} {e}")

    elif cmd[0] == "dir":
        dirlist = os.listdir(cd)
        for i in range(len(dirlist)):
            xprint(dirlist[i], lblue, c)
    
    elif cmd[0] == "cls" or cmd[0] == "clear":
        os.system("cls")

    elif cmd[0] == "echo" and len(cmd) >= 2:
        echo = ""
        for i in range(len(cmd[1:])):
            echo = echo + " " +cmd[i+1]

        xprint(echo.strip(), yellow, c)

    elif cmd[0] == "openfile" and len(cmd) >= 3:
        try:
            if cmd[1] == "/r":
                currentfile = open(cd + cmd[2], "r")
            elif cmd[1] == "/w":
                currentfile = open(cd + cmd[2], "w")
            elif cmd[1] == "/rw":
                currentfile = open(cd + cmd[2], "w+")
            xprint(f"Succesfully opened {cmd[2]}", green, c)
        except Exception as e:
            xprint(f"Unable to open {cd + cmd[2]} {e}", red, c)

    elif cmd[0] == "closefile":
        try:
            currentfile.close()
            xprint("Closed file.", green, c)
        except Exception as e:
            xprint(f"Unable to close file: {e}", red, c)
    
    elif cmd[0] == "writefile" and len(cmd) >= 2:
        try:
            write = ""
            for i in range(len(cmd[1:])):
                write = write + " " + cmd[i+1]
            currentfile.write(write)
            xprint(f"Wrote {write} to currently opened file. ", green, c)
        except Exception as e:
            xprint(f"Error writing to file: {e}", red, c)

    elif cmd[0] == "readfile":
        try:
            xprint(currentfile.read(), yellow, c)
        except Exception as e:
            xprint(f"Couldnt read current file: {e}", red, c)

    elif cmd[0] == "clearfile":
        try:
            currentfile.truncate(0)
            xprint("Cleared file", green, c)
        except Exception as e:
            xprint(f"Error clearing file: {e}", green, c)

    elif cmd[0] == "sys" and len(cmd) >= 2:
        sys = ""
        for i in range(len(cmd[1:])):
            sys = sys + " " + cmd[i+1]
        os.system(f"cd {cd}")
        os.system(sys.strip())

    elif cmd[0] == "run" and len(cmd) >= 2:
        os.startfile(cd + cmd[1])

    elif cmd[0] == "colour" and len(cmd) >= 2:
        try:
            exec(f"currentcol = Colors.{cmd[1]}")
        except Exception as e:
            xprint(f"Error changing color: {e}")

    elif cmd[0] == "unlock":
        devmode = True
        xprint("Unlocked devmode, be careful", Colors.yellow_to_red, "g")

    elif cmd[0] == "chvar":
        if devmode:
            exec(f"{cmd[1]} = {cmd[2]}")
        else:
            xprint("The chvar command is locked, use 'unlock' to unlock.", red, c)

    elif cmd[0] == "exec":
        if devmode:
            execpart = ""
            for i in range(len(cmd[1:])):
                execpart = execpart + " " + cmd[i+1] 
            exec(execpart.strip())
        else:
            xprint("The exec command is locked, use 'unlock' to unlock.", red, c)

    elif cmd[0] == "lock":
        devmode = False
        xprint("Locked devmode", Colors.green_to_cyan, "g")
        