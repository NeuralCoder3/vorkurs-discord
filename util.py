import base64
import requests
import json
import subprocess
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