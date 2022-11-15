import phanim.info as i
from random import randint
import colorama as cl

def printIntro():
    hart = [
    "   _  _ ",
    "  / \/ \ ",
    "  \    / ",
    "   \  / ", 
    "    \/ ",
    # ""
    ]
    print()
    print(cl.Fore.BLUE + f"{i.welcomeMessage(i.name)}")
    print(cl.Fore.GREEN + f"Version: {i.version}")
    print(f"By: {i.author}")
    for row in hart:
        print(cl.Fore.RED + row)
    print(cl.Fore.CYAN + f"{i.quotes[randint(0,len(i.quotes)-1)]}")
    print(cl.Fore.LIGHTYELLOW_EX)