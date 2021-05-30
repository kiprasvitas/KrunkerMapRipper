import undetected_chromedriver.v2 as uc
from pprint import pformat
import base64
from time import sleep
import os
import asyncio
import requests
import json

def scrapeMap(name):

    map_name = name

    res = requests.get('https://api.krunker.io/search?type=map&val=' + map_name)
    response = json.loads(res.text)

    try:
        map_id = response["data"][0]["map_id"]
        map_creator = response["data"][0]["creatorname"]
    except:
        print("no map found")
        return "No map found with that name"

    options = uc.ChromeOptions()
    #options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    options.add_argument("--headless")
    #options.add_argument("--disable-dev-shm-usage")
    #options.add_argument("--no-sandbox")

    driver = uc.Chrome(options=options, enable_cdp_events=True)

    async def main():
        def printResponse(eventdata):
            payload = eventdata['params']['response']['payloadData']
            data = base64.b64decode(payload)
            size = (len(data) * 3) / 4
            if (size > 4000):
                print(data)
                driver.quit()
                return data

        driver.get('https://krunker.io')

        print("website loaded")

        driver.execute_script("selectHostMap('{0}','undefined','{1}','{2}',1)".format(map_name, map_id, map_creator))
        print("host function executed")
        sleep(0.6)

        driver.execute_script("createPrivateRoom()")
        print("started hoster")

        driver.add_cdp_listener("Network.webSocketFrameReceived", printResponse)
        driver.add_cdp_listener("Network.webSocketFrameSent", printResponse)

        await asyncio.sleep(2000)

    asyncio.get_event_loop().run_until_complete(main())