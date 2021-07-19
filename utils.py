import undetected_chromedriver.v2 as uc
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import json
import base64
from time import sleep
import os
import sys
import pprint

def scrapeMap(name):
    map_name = name

    options = uc.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    capabilities = DesiredCapabilities.CHROME
    capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    #executable_path=os.environ.get("CHROMEDRIVER_PATH"), 
    driver = uc.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), patcher_force_close=True, options=options, desired_capabilities=capabilities)

    def process_browser_logs_for_network_events(logs):
        mapdata = "No map data was found. This could be a system failure or it could simply be the map can't be downloaded."
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if ("Network.webSocketFrameReceived" in log["method"]):
                payload = log['params']['response']['payloadData']
                data = base64.b64decode(payload)
                if "init" in str(data):
                    print("Loaded large websocket packet")
                    start = str(data).find('{')
                    end = str(data).rfind(']}') + 2
                    codeu = str(data)[start:end]
                    try:
                        code = codeu.replace(""","col":false""", "")
                    except:
                        print("no occurences of 'col:false;'")
                    print("Successfully loaded map code for {}".format(map_name))
                    mapdata = code
        return mapdata

    driver.get('https://krunker.io/?play={}'.format(map_name))
    print("website loaded")

    sleep(20)

    logs = driver.get_log("performance")

    mapdata = process_browser_logs_for_network_events(logs)

    driver.quit()
    return mapdata