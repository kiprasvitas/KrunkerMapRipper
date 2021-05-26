from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

def runScript(user):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome("C:\\MEGA\\Python\\Krunker API\\Running-Selenium-Script-on-Heroku\\chromedriver.exe", chrome_options=chrome_options)    

    driver.get('https://krunker.io/social.html?p=profile&q=' + user);

    element = WebDriverWait(driver, 30).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[8]/div[5]/div[1]/div[3]")))
    res = driver.find_element_by_xpath('/html/body/div[2]/div[8]/div[5]/div[1]/div[3]')
    res_html = res.get_attribute('outerHTML')
    driver.close()
    return(res_html)
    

    
