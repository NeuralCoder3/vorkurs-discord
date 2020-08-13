import re
import subprocess
import os
from cred import exercisePdfPool
from util import upload3, pdfToPng

def markdownSheet(sheet):
    imagepool=exercisePdfPool

    content=open(sheet).read()
    exercises=[x.group(1).replace(".tex","_png.pdf") for x in re.finditer( r'input{.*?pool/(.*?)}', content)]

    template=open("template.md").read()
    answer=open("answer.md").read()

    content=""
    for ex in exercises:
        imgPathPDF=imagepool+ex
        imgPath=pdfToPng(imgPathPDF)

        imgUrl=upload3(imgPath,"")
        print(imgPath, "=>",imgUrl)
        exText=answer.replace("<<exerciseImage>>", f"![]({imgUrl})")
        content+=exText+"\n\n"

    open("Temp.md","w").write(template.replace("<<content>>", content))


    os.system("curl -v -XPOST -H 'Content-Type: text/markdown' 'https://demo.codimd.org/new' --data-binary @Temp.md > Url.txt")
    url=open("Url.txt").read().replace("Found. Redirecting to ","")+"?both"

    return url