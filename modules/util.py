import base64
import requests
import json
import subprocess
import os

try:
    from .cred import imgbbToken, exercisePdfPool
except ImportError:
    from cred import imgbbToken, exercisePdfPool

def upload3(imgPath,name=""):
    with open(imgPath, "rb") as file:
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": imgbbToken,
            "image": base64.b64encode(file.read()),
        }
        res = requests.post(url, payload)
        return json.loads(res.text)['data']['url']

def pdfToPng(pdfPath):
    imgPath2=pdfPath.replace(".pdf","")
    imgPath=pdfPath.replace(".pdf","-1.png")
    subprocess.call(["pdftoppm", "-png",pdfPath,imgPath2])
    return imgPath

def compileTex(texPath):
    out_dir="."
    process = subprocess.Popen(
        args=[
            f'latexmk',
            f'-pdf',
            f'-outdir={out_dir}',
            f'-pdflatex=pdflatex -interaction=nonstopmode -shell-escape',
            f'-cd', str(texPath)
        ],
        stdout=subprocess.DEVNULL,
        stdin=subprocess.DEVNULL,
        stderr=subprocess.STDOUT)
    process.wait()
    if process.returncode == 0:
        print("Compiled")
        return texPath[:-4]+".pdf"
    else:
        print("Error")
        return None

def dirOfFile(file):
    return os.path.dirname(os.path.abspath(file))+"/"

def compileTexIn(texPath,overviewPath):
    texCode=open(texPath).read()
    overview=open(overviewPath).read()
    path=dirOfFile(texPath)
    tmpPath=path+"TMP.tex"
    file=open(tmpPath,"w")
    file.write(overview.replace("<<<<files>>>>",texCode))
    file.close()
    pdf=compileTex(tmpPath)
    os.unlink(tmpPath)
    return pdf