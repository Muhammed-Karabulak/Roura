from os import system, chdir, listdir, mkdir, getcwd
from shutil import move
from pathlib import Path

from keyboard import press, write
from time import sleep

from rich.console import Console
from Modules.Param import Param        
       
console = Console()                

class Commands:
    def organizeFiles(self):
        """Creates folders by file extensions in the user-provided directory."""
        path = input("  Path :")
        if path == "pass":
            return
        
        startDir = getcwd()
        chdir(path)

        files = listdir(path)

        for file in files:
            if Path(f"{getcwd()}//{file}").is_file():
                f = file.split(".")
                try:
                    mkdir(f"{f[len(f) - 1]}".upper() + "'s")
                except FileExistsError:
                    pass
                
                move(file, f"{f[len(f) - 1]}".upper() + "'s")
            
        chdir(startDir)
        console.print(f"Organization Complite.", style="bold green") 


    def find(self, search : Param = None):
        """Opens the search box in the active application and optionally types provided text."""
        press("F3")
        if search:
            sleep(0.1)
            write(str(search))    
    
class CommadSystem:
    def __init__(self, kill_fonk, SplitWord = "and"):
        """Initializes the command manager, preparing default and parameterized command tables."""
        self.startDir = getcwd()         
        
        self.lastCommads = []
        
        self.SplitWord = SplitWord.strip()
        
        self.Active = True        
        self.printFlag = True    

        # Rora's Commads
        self.notParameterizedCommands = {
            "clear" : (lambda: system("cls")),
            # Closing Roura
            "kill" : kill_fonk,
            # Clear Console
            "clear" : (lambda: system("cls")),
            # Organize Files In Path
            "organize" : Commands.organizeFiles,            
            # Open Youtube Music       
            "music" : (lambda: system("start https://music.youtube.com")),
            # Open Youtube
            "youtube" : (lambda: system("start https://youtube.com")),            
            
            # Pressing F3
            "find" : Commands.find,
            
            # Change Print State
            "don't print" : (lambda: self.printFlagChange(False)),
            # Chance Print State
            "print" : (lambda: self.printFlagChange(True)),         
        }
        
        self.parameterizedCommands = {      
            # Search A Word Or Sentence On Internet
            "search" : (lambda args: system("start https://search.brave.com/search?q={}".format(args.strForLink()))),
            
            # search some thing in youtube
            "youtube" : (lambda args: system("start https://www.youtube.com/results?search_query={}".format(args.strForLink()))),
            # search some thing in youtube music
            "music" : (lambda args: system("start https://music.youtube.com/search?q={}".format(args.strForLink()))),
            
            # Find A Word Or Sentence From In Page
            "find" : (lambda args: Commands.find(args)),
        }
        
    def getLastCommad(self) -> str:
        """Returns the list of last executed commands."""
        return self.lastCommads
    
    def printFlagChange(self, state : bool):
        """Toggles whether commands are printed to the console."""
        self.printFlag = state        
                
    def addCommad(self, func : set, haveParameter = False) -> None:
        """Adds new commands to the default or parameterized lists from external callers."""
        if haveParameter:
            self.parameterizedCommands.update(func)
        else:
            self.notParameterizedCommands.update(func)
            
            
    def debug(self, commandType : str) -> None:
        match commandType:
            case "eval":                
                try:
                    with open(input("Path :"), "r") as file:
                        eval(compile(file.read(), "<string>", "eval"))
                except Exception as ex:
                    print(ex)
            case "exec":                    
                try:
                    with open(input("Path :"), "r") as file:
                        exec(compile(file.read(), "<string>", "exec"))
                except Exception as ex:
                    print(ex)   
            case "single":
                try:
                    with open(input("Path :"), "r") as file:
                        exec(compile(file.read(), "<string>", "single",))
                except Exception as ex:
                    print(ex) 
            case _:
                print("Wrong Val")
                
            
    def Request(self, text: str) -> None:
        """Splits incoming text into commands and executes matching commands
        with appropriate parameters."""
        
        self.lastCommads.clear()
        
        if self.printFlag:
            console.print(f"[b]{text}[/b]")
            
        reqCommands = [x.strip() for x in text.split("and")]
        
        for reqCommand in reqCommands:
            partialText = reqCommand.split(" ")
            
            first2Word = partialText[0] + " " + partialText[1] if len(partialText) >= 2 else None
            first3Word = partialText[0] + " " + partialText[1] + " " + partialText[2] if len(partialText) >= 3 else None
            
            params = {
                "commad" : "",
                "is defult commad" : False,
                "is parameter command" : False,
                "params" : ""
            }            
            
            if partialText[0] in self.notParameterizedCommands:
                params["commad"] = partialText[0]
                params["is defult commad"] = True
                
            elif first2Word in self.notParameterizedCommands:
                params["commad"] = first2Word
                params["is defult commad"] = True      

            elif first3Word in self.notParameterizedCommands:
                params["commad"] = first3Word
                params["is defult commad"] = True
                
            if partialText[0] in self.parameterizedCommands:
                params["commad"] = partialText[0]
                params["is parameter command"] = True
                params["params"] = partialText[1:]    
                        
            elif first2Word in self.parameterizedCommands:
                params["commad"] = first2Word
                params["is parameter command"] = True
                params["params"] = partialText[2:]
            
            elif first3Word in self.parameterizedCommands:
                params["commad"] = first3Word
                params["is parameter command"] = True
                params["params"] = partialText[3:]
                
            
            if params["is defult commad"] and not params["is parameter command"]:
                self.notParameterizedCommands[params["commad"]]()                
                self.lastCommads.append(params["commad"])
                
            elif params["is parameter command"] and not params["is defult commad"]:
                self.parameterizedCommands[params["commad"]](Param(params["params"]))                
                self.lastCommads.append(params["commad"])
                
            elif params["is defult commad"] and params["is parameter command"]:
                if params["params"]:
                    self.parameterizedCommands[params["commad"]](Param(params["params"]))
                    self.lastCommads.append(params["commad"])
                else:
                    self.notParameterizedCommands[params["commad"]]()
                    self.lastCommads.append(params["commad"])
            
            
            
        
