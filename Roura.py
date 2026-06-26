from sys import executable, argv
from os import execv
from threading import Thread

from Modules import CommandSys
from Modules.CommandSys import CommadSystem
from Modules.SpeechToText import SpeechToText
from Modules.TextToSpeech import TextToSpeech

class Roura:
    """Main controller class that listens for voice commands
    and converts them into application commands."""
    def __init__(self):
        """Initializes the command system, speech recognition,
        and text-to-speech components."""
        
        self.CSYS = CommadSystem(self.kill)
        self.STT = SpeechToText(on_final=self.processRequest)
        self.TTS = TextToSpeech()
        
        self.VoiceRequestFlag = True     
        self.SoundFlag = True
        
        
    def kill(self):
        """Stops the speech capture stream."""
        self.STT.stop()
        
        
    def restart(self):
        """Restarts the running Python process with the same arguments."""
        self.TTS.play("Restarting")
        python = executable
        execv(python, [python] + argv)
            
            
    def complationSpeech(self, req: str):
        """Constructs spoken feedback text based on completed commands."""
        match req:
            case "kill":
                text = "Have a Good Day"
            case "clear computer":
                text = "Computer Cleared"
            case "music":
                text = "WebSite Opened"
            case "youtube":
                text = "WebSite Opened"
            case "do not print":
                text = "Not Printing"
            case "print":
                text = "Printing"
            case _:
                text = f"{req} is Complate"

        Thread(target=self.TTS.play, args=(text,), daemon=True).start()
        
    def addCommad(self, func : set, HaveParametr = False):
        """Adds new command functions to the command system."""
        self.CSYS.addCommad(func, HaveParametr)
        
    def commandByHand(self, commad : str):
        """Processes a command entered by keyboard through the normal request flow."""
        self.processRequest(commad)
        
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
                self.print("Wrong Val")
        
    def ControlCommads(self, req: str):
        """Manages the assistant's own control commands (restart/open/close/debug)."""
        if req == "restart":
            self.restart()
        elif req == "close":
            self.VoiceRequestFlag = False
            self.TTS.play("Good Days")
        elif req == "open":
            self.VoiceRequestFlag = True
            self.TTS.play("How Can I Help You")
        elif req.split(" ")[0] == "debug":
            self.debug(req.split(" ")[1])
            
            
    def processRequest(self, text : str):
        """Validates incoming text and forwards it to the command system if active."""
        self.ControlCommads(text)        
        
        if self.VoiceRequestFlag:   
            self.CSYS.Request(text)
            self.VoiceRequest(self.CSYS.getLastCommad())
        
        
    def VoiceRequest(self, req: str):
        """Speaks out executed commands as vocal feedback."""
        if len(req) == 1:                    
            self.complationSpeech(req[0])
        elif len(req) > 1:
            self.complationSpeech(" and ".join(req))                
        
    def loop(self):
        """Runs the assistant's continuous listening and command-processing loop."""
        try:
            self.CSYS.notparameterizedCommands["clear"]()
            self.STT.start()
            
            while True:
                self.STT.CatchSpeech()                   
                        
        except KeyboardInterrupt:
            self.kill()
            
    def start(self):
        """Public start method called externally."""
        self.loop()
            
          
if __name__ == "__main__":
    r = Roura()
    r.loop()