import os
try:
    from .credPrivate import *
except ImportError:
    from credPrivate import *

def findPath(p,abs=False):
    if not os.path.exists(p):
        if abs:
            p=os.getcwd()+p
        else:
            p="."+p
        if not os.path.exists(p):
            try:
                folder=os.path.dirname(p)
                print("create",folder)
                os.makedirs(folder)
            except:
                pass
    return p

# URLs

miroUrl="https://miro.com/app/board/"
# codiUrl="https://dpad.cs.uni-saarland.de/"
# no access

# Files and placeholders

database="data.db"
boardFile="boards.txt"
aliasFile="defaultAlias.txt"
downDir=findPath("/storage/",True)


# Data

warmupTime=(10,1)
scheduleTime=(10,2)
hourOff=0

tutorialTime=(13,50)

# for weekends
datemap=[
    "A1","A2","A3","A4","A5","","",
    "B1","B2","B3","B4","B5","","",
    "C1","C2","C3","C4","C5","","",
    "D1","D2","D3","D4","D5","","",
    "","","","","",
    "","","","","",
    "","","","","",
    "","","","","",
    "","","","",""
]

tutorialmap= (
    # Week 1
    ["Sprachen"]*2+ 
    ["Aussagenlogik"]+
    ["Prädikatenlogik"]*4+  
    # Week 2 
    ["Beweisen"]*2+ 
    ["Textbeweise"]*5+ 
    # Week 3
    ["Mengen"]+ 
    ["Relationen"]*6+ 
    # Week 4
    ["Induktion"]*7
)
