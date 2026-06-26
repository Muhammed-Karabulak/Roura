from Modules.CommandSys import CommadSystem

c = CommadSystem(print)

while True:
    req = input("::>")
    c.Request(req)