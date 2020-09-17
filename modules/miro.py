from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests

try:
    from .util import upload3, pdfToPng
    # from .cred import profileDir,browser
    from .cred import miroUrl, miroOAuth
    from .import database as db
except ImportError:
    from util import upload3, pdfToPng
    # from cred import profileDir,browser
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

    # print(response.text)
    return print(response.json()["id"])


def getUrl(boardId):
    # return miroUrl+boardId+"/"
    return boardId

def addPdf(pdf,boardId):
    cached=db.lookupCache(pdf)
    if cached is not None:
        imgUrl=cached
    else:
        imgPath=pdfToPng(pdf)
        imgUrl=upload3(imgPath)
        db.storeCache(pdf,imgUrl)
    addImageUrl(imgUrl,boardId)

def addImageUrl(imgUrl,boardId):
    # chrome_options = Options()
    # chrome_options.add_argument("--user-data-dir="+profileDir) 
    # chrome_options.add_argument('--profile-directory=Profile 1')
    # chrome_options.binary_location=(browser)
    # driver = webdriver.Chrome(options=chrome_options)
    url=getUrl(boardId)

    # options = Options()

    # # options.add_argument("--user-data-dir="+profileDir) 
    # # options.add_argument('--profile-directory=Profile 1')
    # # options.binary_location=(browser)

    # options.add_argument('headless')
    # # options.add_argument('--headless')
    # # options.add_argument("--no-sandbox")
    # # options.add_argument("window-size=1400,2100") 
    # # options.add_argument('--disable-gpu')
    # driver = webdriver.Chrome(options=options)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--window-size=1420,1080')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(chrome_options=chrome_options)


    # driver = webdriver.Chrome()

    driver.get(url)

    # to wait til done

    # from selenium.webdriver.support.ui import WebDriverWait
    # from selenium.webdriver.support import expected_conditions as EC

    # try:
    #     myElem = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    #     print "Page is ready!"
    # except TimeoutException:
    #     print "Loading took too much time!"
    time.sleep(10)

    # print("Insert")
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

    time.sleep(5)
    driver.close()


def uploadWarmup(sheetPdf,boardId):
    addPdf(sheetPdf,boardId)
    return getUrl(boardId)