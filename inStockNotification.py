# Stock Checker and Notifier
# 
# Created by Hugo Garcia 2020
# With the help of the following article:
# https://medium.com/better-programming/lets-create-an-instagram-bot-to-show-you-the-power-of-selenium-349d7a6744f7

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import random
from datetime import datetime
import http.client
import urllib

def sendPushover(appToken, userToken, messageToSend):
    # Send Pushover notification
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": appToken,
            "user": userToken,
            "message": messageToSend,
        }), { "Content-type": "application/x-www-form-urlencoded" })
    conn.getresponse()

def checkHaleyStock(website, appToken, userToken):
    # If webdriver.Chrome() throws an error, then that means you need to install
    # Chrome Driver from: http://chromedriver.chromium.org/downloads
    # Make sure to select the correct version
    #
    # If chromedriver.exe is located somewhere other than the same directory
    # as this python file, then specify the location below.
        
    try:
        browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        browser.get(website)

        # Wait for page to load to ensure newsletter popup comes up
        time.sleep(2)

        # Press ESC key to click out of newsletter popup
        ActionChains(browser).send_keys(Keys.ESCAPE).perform()

        #time.sleep(2)

        # Check to see which models are missing the 'out-of-stock' class name
        inStock = browser.find_elements_by_xpath('//div[@class="swatch-option__wrapper"]')
        #inStock = browser.find_elements_by_class_name('swatch-option__wrapper')

        if len(inStock) > 0:
            modelsInStock = []

            # Create list of models that are in stock
            for model in inStock:
                modelsInStock.append(model.text)
            
            print("Haley " + dt_string + " (" + randDelayStr + ") : ")
            print(*modelsInStock, sep = ", ")
            sendPushover(appToken, userToken, modelsInStock)
            
        else:
            print("Haley " + dt_string + " (" + randDelayStr + ") : Out of Stock")
        

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print("Moving on..")
        print()
        sendPushover(appToken, userToken, "Haley site failed to load.")

    finally:
        # Close browser when done
        browser.quit()


def checkTRexStock(website, appToken, userToken):
    # If webdriver.Chrome() throws an error, then that means you need to install
    # Chrome Driver from: http://chromedriver.chromium.org/downloads
    # Make sure to select the correct version
    #
    # If chromedriver.exe is located somewhere other than the same directory
    # as this python file, then specify the location below.
    
    try:
        browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        browser.get(website)

        # Wait for page to load to ensure newsletter popup comes up
        time.sleep(3)

        # Select color from dropdown
        dropdownColor = Select(browser.find_element_by_id("pa_Color")) 
        #print([o.text for o in dropdownColor.options])
        dropdownColor.select_by_visible_text("Ranger")

        time.sleep(2)

        # Select size from dropdown
        dropdownSize = Select(browser.find_element_by_id("pa_Size")) 
        #print([o.text for o in dropdownSize.options])
        dropdownSize.select_by_visible_text("Medium")

        time.sleep(2)

        # See if selected color and size are in stock
        inStock = browser.find_element_by_xpath('//div[contains(@class, "woocommerce-variation-availability")]').text
        #inStock = browser.find_elements_by_class_name('swatch-option__wrapper')
        #print(inStock)

        if inStock == "Out of stock":
            print("T-Rex " + dt_string + " (" + randDelayStr + ") : Out of Stock")
            
        else:
            print("T-Rex " + dt_string + " (" + randDelayStr + ") : In Stock!")
            sendPushover(appToken, userToken, "Orion belt in stock!")

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print("Moving on..")
        print()
        sendPushover(appToken, userToken, "TRex Arms site failed to load.")

    finally:
        # Close browser when done
        browser.quit()

var = 1

while var == 1 :
    # Generate a random number within a range
    randDelay = random.randint(600,1200)
    randDelayStr = str(int(round(randDelay/60))) + "mins"
    
    now = datetime.now()
    # dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    checkHaleyStock('https://haleystrategic.com/shop/soft-goods/chestrigs/d3crm-micro', **APPTOKEN**, **USER TOKEN**)

    time.sleep(3)

    checkTRexStock('https://www.trex-arms.com/store/t-rex-arms-orion/', **APPTOKEN**, **USER TOKEN**)
    
    # Delay next try by pseudo-random time
    time.sleep(randDelay)
    #var = 0

print('Goodbye')
