import undetected_chromedriver.v2 as uc
import base64
from time import sleep
import os
import asyncio
import requests
import json

websocket_count = 0;

def scrapeMap(name):
    map_name = name

    options = uc.ChromeOptions()
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options, enable_cdp_events=True)

    async def main():
        def printResponse(eventdata):
            global websocket_count
            payload = eventdata['params']['response']['payloadData']
            data = base64.b64decode(payload)
            size = (len(data) * 3) / 4
            if (size > 4000):
                print("Loaded large websocket packet")
                try:
                    start = str(data).find('{')
                except:
                    print("error parsing data (start)")
                    driver.quit()
                    return "error parsing data (start)"
                try:
                    end = str(data).rfind(']}') + 2
                except:
                    print("error parsing data (end)")
                    driver.quit()
                    return "error parsing data (end)"
                print("end of file: {}".format(end))
                codeu = str(data)[start:end]
                try:
                    code = codeu.replace(""","col":false""", "")
                except:
                    print("no occurences of 'col:false;'")
                print("Successfully loaded map code for {}".format(map_name))
                driver.quit()
                return code
            elif (websocket_count < 10):
                websocket_count = websocket_count + 1
            else:
                print("No map data to return")
                driver.quit()
                return "No map data was found at given map name."

        driver.get('https://krunker.io/?play={}'.format(map_name))
        print("website loaded")

        driver.add_cdp_listener("Network.webSocketFrameReceived", printResponse)
        driver.add_cdp_listener("Network.webSocketFrameSent", printResponse)

        await asyncio.sleep(2000)

    asyncio.get_event_loop().run_until_complete(main())