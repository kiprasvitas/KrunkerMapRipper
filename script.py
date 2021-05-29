import undetected_chromedriver.v2 as uc
from pprint import pformat
import base64
import os
import asyncio

options = uc.ChromeOptions()
#options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")

#options.add_argument("--headless")
#options.add_argument("--disable-dev-shm-usage")
#options.add_argument("--no-sandbox")

driver = uc.Chrome(options=options, enable_cdp_events=True)

async def main():
    def printResponse(eventdata):
        payload = eventdata['params']['response']['payloadData']
        data = base64.b64decode(payload)
        print(payload)

    driver.get('https://krunker.io')

    driver.add_cdp_listener("Network.webSocketFrameReceived", printResponse)
    driver.add_cdp_listener("Network.webSocketFrameSent", printResponse)

    await asyncio.sleep(2000)

asyncio.get_event_loop().run_until_complete(main())