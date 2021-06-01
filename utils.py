import undetected_chromedriver.v2 as uc
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
    options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

    options.add_argument("--headless")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=options, enable_cdp_events=True)

    async def main():
        def printResponse(eventdata):
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

        driver.get('https://krunker.io')

        print("website loaded")
        sleep(2)

        try:
            driver.execute_script("selectHostMap('{0}','undefined','{1}','{2}',1)".format(map_name, map_id, map_creator))
            print("host function executed")
            sleep(1)
        except:
            driver.quit()
            return "failed operation at host map"

        driver.execute_script("createPrivateRoom()")
        print("started hoster")

        driver.add_cdp_listener("Network.webSocketFrameReceived", printResponse)
        driver.add_cdp_listener("Network.webSocketFrameSent", printResponse)

        await asyncio.sleep(2000)

    asyncio.get_event_loop().run_until_complete(main())