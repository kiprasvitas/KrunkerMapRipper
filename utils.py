import undetected_chromedriver.v2 as uc
import base64
from time import sleep
import os
import asyncio
import requests
import json
import sys

websocket_count = 0
returnvalue = "Couldn't load map data. Try again."

def scrapeMap(name):
    map_name = name

    options = uc.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), keep_alive=True, version_main=90, patcher_force_close=True, options=options, enable_cdp_events=True)

    def printResponse(eventdata):
        global websocket_count
        global returnvalue
        payload = eventdata['params']['response']['payloadData']
        data = base64.b64decode(payload)
        size = (len(data) * 3) / 4
        if (size > 4000 and returnvalue == "Couldn't load map data. Try again."):
            print("Loaded large websocket packet")
            start = str(data).find('{')
            end = str(data).rfind(']}') + 2
            print("end of file: {}".format(end))
            codeu = str(data)[start:end]
            try:
                code = codeu.replace(""","col":false""", "")
            except:
                print("no occurences of 'col:false;'")
            print("Successfully loaded map code for {}".format(map_name))
            returnvalue = code

        elif (websocket_count < 40 and returnvalue == "Couldn't load map data. Try again."):
            websocket_count = websocket_count + 1
        else:
            if (returnvalue == "Couldn't load map data. Try again."):
                print("No map data to return")
                returnvalue = "No map data was found at given map name."

    with driver:
        driver.add_cdp_listener("Network.webSocketFrameReceived", printResponse)
        driver.add_cdp_listener("Network.webSocketFrameSent", printResponse)
        driver.get('https://krunker.io/?play={}'.format(map_name))
        print("website loaded")

    sleep(10)
    driver.quit()
    return returnvalue