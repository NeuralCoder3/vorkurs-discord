import os
try:
    from .credPrivate import *
except ImportError:
    from credPrivate import *

def findPath(p):
    if not os.path.exists(p):
        return "."+p
    else:
        return p

miroUrl="https://miro.com/app/board/"
database="data.db"
boardFile="boards.txt"

gitRepo=findPath("/storage/material/")
overviewPNG=gitRepo+"sheets/warmup/pool/overviewPNG.tex"
sheetFolder="sheets/warmup/2019/"
sheetPlaceholder="SHEET_ID"
sheetTex=gitRepo+sheetFolder+f"warmup_{sheetPlaceholder}.tex"

# codiUrl="https://dpad.cs.uni-saarland.de/"
# no access
