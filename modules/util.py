import base64
import requests
import json
import subprocess
import os
import dropbox
import uuid

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions

try:
    from .cred import imgbbToken, downDir
    from .credPrivate import userName, userPwd, dropbox_token
except ImportError:
    from cred import imgbbToken, downDir
    from credPrivate import userName, userPwd, dropbox_token

class TransferData:
    def __init__(self, access_token):
        self.access_token = access_token

    def upload_file(self, file_from, file_to):
        dbx = dropbox.Dropbox(self.access_token)

        with open(file_from, 'rb') as f:
            dbx.files_upload(f.read(), file_to)

        return dbx.sharing_create_shared_link_with_settings(file_to).url.replace("dl=0","dl=1")

def upload4(imgPath,name="TMP"):
    transferData = TransferData(dropbox_token)

    file_from = imgPath
    file_to = '/Apps/Test-Vokurs2/'+name+str(uuid.uuid4())+".png"

    url= transferData.upload_file(file_from, file_to)
    # print(url)
    return url

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
    imgPath3=pdfPath.replace(".pdf","-*")
    imgPath=pdfPath.replace(".pdf",".png")
    subprocess.call(["pdftoppm", "-png",pdfPath,imgPath2])
    subprocess.call(["convert", "+append",imgPath3,imgPath])
    # subprocess.call(["rm", imgPath3])
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


def getCurrentPDFFile():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    prefs = {'download.default_directory' : downDir}
    chrome_options.add_argument("download.default_directory="+downDir)
    chrome_options.add_experimental_option('prefs', prefs)
    driver = webdriver.Chrome(chrome_options=chrome_options)

    driver.get("https://vorkurs.cs.uni-saarland.de/cms/ss20/users/login")

    try:
        myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'UserUsername')))
    except TimeoutException:
        print("Loading took too much time!")

    driver.implicitly_wait(1)

    driver.execute_script("document.getElementsByName('data[User][username]')[1].value='"+userName+"';")
    driver.execute_script("document.getElementsByName('data[User][password]')[1].value='"+userPwd+"';")


    driver.find_element_by_xpath("//*[@value='Login']").click()

    driver.get("https://vorkurs.cs.uni-saarland.de/cms/ss20/materials/")

    elem=[(e.text,e.get_attribute("href")) for e in driver.find_elements_by_tag_name("a") if "Warmup" in e.text and "ung" not in e.text]
    link=sorted(elem)[-1][1]
    driver.get(link)
    fileName=link.split("/")[-1]
    return downDir+fileName
