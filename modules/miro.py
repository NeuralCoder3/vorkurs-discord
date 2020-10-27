from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import time
import requests
import os
from random import randint

try:
    from .util import upload4, pdfToPng, getBrowser
    from .cred import miroUrl, miroOAuth
    from .import database as db
except ImportError:
    from util import upload4, pdfToPng, getBrowser
    from cred import miroUrl, miroOAuth
    import database as db


def createBoard(name):
    url = "https://api.miro.com/v1/boards"

    payload = "{\"name\":\""+name+"\",\"sharingPolicy\":{\"access\":\"view\",\"teamAccess\":\"edit\"}}"
    headers = {
        'content-type': "application/json",
        'authorization': "Bearer "+miroOAuth
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    return print(response.json()["id"])


def getUrl(boardId):
    return boardId+"?rnd="+str(randint(0,42))

def addPdf(pdf,boardId,uploadTime):
    cached=db.lookupCache(pdf)
    if cached is not None:
        imgUrl=cached
    else:
        imgPath=pdfToPng(pdf)
        imgUrl=upload4(imgPath)
        db.storeCache(pdf,imgUrl)
    addImageUrl(imgUrl,boardId,uploadTime)

def addImageUrl(imgUrl,boardId, uploadTime):
    url=getUrl(boardId)

    driver=getBrowser()

    # options = FirefoxOptions()
    # options.headless = True
    # driver = webdriver.Firefox(options=options) #, executable_path=r'C:\Utility\BrowserDrivers\geckodriver.exe')

    driver.get(url)

    # to wait til done
    # try:
    #     myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    # except TimeoutException:
    #     print "Loading took too much time!"
    time.sleep(10)

    # for brave
    # driver.find_element_by_class_name("toolbar__item--upload").click()

    # for chrome
    driver.find_element_by_class_name("AT__toolbar--LIBRARY").click()
    time.sleep(0.5)
    driver.find_element_by_class_name("AT__library--UPLOAD").click()
    time.sleep(0.5)

    driver.find_element_by_xpath("//*[@data-autotest-id='AT__upload--upload_via_url']").click()

    driver.find_element_by_xpath("//*[@data-autotest-id='modal-window__input']").send_keys(imgUrl)
    driver.find_element_by_xpath("//*[@data-autotest-id='modal-window__submit-button']").click()

    time.sleep(uploadTime)
    try:
        driver.close()
    except:
        pass


def uploadWarmup(sheetPdf,boardId,uploadTime=20):
    addPdf(sheetPdf,boardId,uploadTime)
    return getUrl(boardId)
