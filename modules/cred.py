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
            print(f"We have a problem: {p} does not exists.")
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
# gitRepo=findPath("/storage/materials/")
# overviewPNG=gitRepo+"sheets/warmup/pool/overviewPNG.tex"
# sheetFolder="sheets/warmup/2020/"
# sheetPlaceholder="SHEET_ID"
# sheetTex=gitRepo+sheetFolder+f"warmup_{sheetPlaceholder}.tex"


# Data

warmupTime=(10,1)
scheduleTime=(10,1)

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