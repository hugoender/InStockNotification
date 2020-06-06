# Stock Checker and Notifier
# 
# Created by hugoender 2020
# With the help of the following article:
# https://medium.com/better-programming/lets-create-an-instagram-bot-to-show-you-the-power-of-selenium-349d7a6744f7

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime
import http.client, urllib

class StockCheckerBot():
    def __init__(self, website, appToken, userToekn):
        # If webdriver.Chrome() throws an error, then that means you need to install
        # Chrome Driver from: http://chromedriver.chromium.org/downloads
        # Make sure to select the correct version
        #
        # If chromedriver.exe is located somewhere other than the same directory
        # as this python file, then specify the location below.
        self.browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        self.browser.get(website)

        # Wait for page to load to ensure newsletter popup comes up
        time.sleep(3)

        # Press ESC key to click out of newsletter popup
        ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

        # Check to see which models are missing the 'out-of-stock' class name
        inStock = self.browser.find_elements_by_xpath('//div[@class="swatch-option__wrapper"]')
        #inStock = self.browser.find_elements_by_class_name('swatch-option__wrapper')

        if len(inStock) > 0:
            modelsInStock = []
            
            # Create list of models that are in stock
            for model in inStock:
                modelsInStock.append(model.text)
                print(dt_string + ": " + modelsInStock)
            
            # Send Pushover notification
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                urllib.parse.urlencode({
                    "token": appToken,
                    "user": userToken,
                    "message": modelsInStock,
                }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()
        else:
            print(dt_string + ": Out of Stock")

        # Close browser when done
        self.browser.quit()

var = 1

while var == 1 :
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    bot = StockCheckerBot('https://haleystrategic.com/shop/soft-goods/chestrigs/d3crm-micro', '123456', '78910')
    
    time.sleep(300)
    #var = 0

print('Goodbye')