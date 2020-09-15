import re
import subprocess
import os

try:
    from .util import upload3, pdfToPng, dirOfFile, compileTexIn
    from .cred import overviewPNG
    from .import database as db
except ImportError:
    from util import upload3, pdfToPng, dirOfFile, compileTexIn
    from cred import overviewPNG
    import database as db


def createFromFile(filePath):
    os.system("curl -v -XPOST -H 'Content-Type: text/markdown' 'https://demo.codimd.org/new' --data-binary @"+filePath+" > Url.txt")
    url=open("Url.txt").read().replace("Found. Redirecting to ","")+"?both"
    return url


def markdownSheet(sheet,number):
    content=open(sheet).read()
    # exercises=[x.group(1).replace(".tex","_png.pdf") for x in re.finditer( r'input{.*?pool/(.*?)}', content)]

    content=content.replace("\squestion","\input{../pool/kennenlernen/self.tex}")
    content= re.sub(r'\\begin{secretquestions}(?s:.)*?\\end{secretquestions}', '', content)

    exercises=[x.group(1) for x in re.finditer( r'input{(.*?pool/.*?)}', content)]
    exercises=[os.path.abspath(dirOfFile(sheet)+x) for x in exercises]

    template=open("template.md").read()
    answer=open("answer.md").read()
    
    header=open("markdownHeader.md").read()
    template=template.replace("<<header>>",header)
    template=template.replace("<<number>>",number)

    content=""
    for ex in exercises:
        # print(ex)
        cached=db.lookupCache(ex)
        if cached is not None:
            imgUrl=cached
        else:
            imgPathPDF=compileTexIn(ex,overviewPNG)
            imgPath=pdfToPng(imgPathPDF)

            imgUrl=upload3(imgPath,"")
            db.storeCache(ex,imgUrl)
            print(ex, "=>",imgUrl)

        exText=answer.replace("<<exerciseImage>>", f"![]({imgUrl})")
        content+=exText+"\n\n"

    open("Temp.md","w").write(template.replace("<<content>>", content))

    url=createFromFile("Temp.md")
    return url