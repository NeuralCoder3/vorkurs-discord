from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
from util import upload3, pdfToPng
from cred import boardUrl, profileDir,browser


def uploadWarmup(sheetPdf):
    imgPath=pdfToPng(sheetPdf)
    imgUrl=upload3(imgPath)

    url=boardUrl
    chrome_options = Options()
    chrome_options.add_argument("--user-data-dir="+profileDir) 
    chrome_options.add_argument('--profile-directory=Profile 1')
    chrome_options.binary_location=(browser)
    driver = webdriver.Chrome(options=chrome_options)
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

    print("Loaded")

    driver.find_element_by_class_name("toolbar__item--upload").click()

    # data-autotest-id="AT__upload--upload_via_url"

    driver.find_element_by_xpath("//*[@data-autotest-id='AT__upload--upload_via_url']").click()

    # driver.find_element_by_xpath("//*[@data-autotest-id='modal-window__input']").setAttribute("value", "")
    driver.find_element_by_xpath("//*[@data-autotest-id='modal-window__input']").send_keys(imgUrl)
    driver.find_element_by_xpath("//*[@data-autotest-id='modal-window__submit-button']").click()

    
    # time.sleep(2)
    # driver.find_element_by_id("active_users_layer").send_keys(Keys.PAGE_DOWN)
    # Actions builder = new Actions(driver);
    # builder.keyDown(Keys.PAGE_DOWN).perform()
    # driver.find_element_by_xpath('//body').send_keys(Keys.PAGE_DOWN)

    return url
    # 