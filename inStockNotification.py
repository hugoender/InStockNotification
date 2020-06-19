# Stock Checker and Notifier
# 
# Created by hugoender 2020
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
import sys


try:
    minIntervalArg = sys.argv[1]
    maxIntervalArg = sys.argv[2]
except IndexError:
    raise SystemExit(f"Usage: {sys.argv[0]} <min interval in seconds> <max interval in seconds>")


def Diff(li1, li2): 
    # Python code to get difference of two lists 
    # Using set() 
    return (list(set(li1) - set(li2))) 

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

def checkHaleyChestRigStock(website, desiredModel, appToken, userToken):
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

        # Check to see which models are missing the 'out-of-stock' class name
        inStock = browser.find_elements_by_xpath('//div[@class="swatch-option__wrapper"]')

        if len(inStock) > 0:
            modelFound = 0
            modelsInStock = []

            # Create list of models that are in stock
            for model in inStock:
                modelsInStock.append(model.text)
                # Check if it's desired model
                if model.text == desiredModel:
                    modelFound = 1
            
            print("Haley " + datetime_string + " (" + randDelayStr + ") : ")
            print(*modelsInStock, sep = ", ")
            
            if modelFound:
                sendPushover(appToken, userToken, modelsInStock)
            
        else:
            print("Haley " + datetime_string + " (" + randDelayStr + ") : Out of Stock")
        

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print("Moving on..")
        print()
        sendPushover(appToken, userToken, "Haley site failed to load.")

    finally:
        # Close browser when done
        browser.quit()

def checkHaleySMGStock(website, productSKU, appToken, userToken):
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

        try:
            # Check to see if it has two Out of Stock elements which would indicate it's out of stock
            #addToCartButton = browser.find_elements_by_xpath('//form[@data-product-sku="' + productSKU + '"]//div[@class="addon-product__out_of_stock"]')
            addToCartButton = browser.find_element_by_xpath('//div[contains(@class, "hs-input__add-to-cart")]').text

            if addToCartButton:      
                pushoverText = productSKU + " is in stock :)))"      
                print("Haley " + datetime_string + " (" + randDelayStr + ") : " + pushoverText)
                sendPushover(appToken, userToken, pushoverText)
                
            else:
                print("Haley " + datetime_string + " (" + randDelayStr + ") : Out of Stock")

        except Exception:
            print("Haley " + datetime_string + " (" + randDelayStr + ") : Out of Stock")
            

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
        dropdownColor.select_by_visible_text("Ranger")

        time.sleep(2)

        # Select size from dropdown
        dropdownSize = Select(browser.find_element_by_id("pa_Size")) 
        dropdownSize.select_by_visible_text("Medium")

        time.sleep(2)

        # See if selected color and size are in stock
        inStock = browser.find_element_by_xpath('//div[contains(@class, "woocommerce-variation-availability")]').text

        if inStock == "Out of stock":
            print("T-Rex " + datetime_string + " (" + randDelayStr + ") : Out of Stock")
            
        else:
            print("T-Rex " + datetime_string + " (" + randDelayStr + ") : In Stock!")
            sendPushover(appToken, userToken, "Orion belt in stock!")

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print("Moving on..")
        print()
        sendPushover(appToken, userToken, "TRex Arms site failed to load.")

    finally:
        # Close browser when done
        browser.quit()

def checkCoyoteStock(website, listOfPreviousItems, appToken, userToken):
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

        # See if selected color and size are in stock
        itemsFound = browser.find_elements_by_xpath('//span[@class="ProductName"]')

        listOfCurrentItems = []

        # Create list of models that are in stock
        for item in itemsFound:
            listOfCurrentItems.append(item.text)

        newItems = Diff(listOfCurrentItems, listOfPreviousItems)

        if newItems:
            print("Coyote " + datetime_string + " (" + randDelayStr + ") : ")
            print(*newItems, sep = ", ")
            sendPushover(appToken, userToken, newItems)
            
        else:
            print("Coyote " + datetime_string + " (" + randDelayStr + ") : No change")

    except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print("Moving on..")
        print()
        sendPushover(appToken, userToken, "Coyote site failed to load.")

    finally:
        # Close browser when done
        browser.quit()
        return listOfCurrentItems

var = 1

listOfPreviousItems = []

while var == 1 :
    # Generate a random number within a range of values specified in command line arguments
    randDelay = random.randint(int(minIntervalArg),int(maxIntervalArg))
    randDelayStr = str(int(round(randDelay/60))) + "mins"
    
    now = datetime.now()
    # dd/mm/YY H:M:S
    datetime_string = now.strftime("%d/%m/%Y %H:%M:%S")
    
    #checkHaleyChestRigStock('https://haleystrategic.com/shop/soft-goods/chestrigs/d3crm-micro', "Black", **APPTOKEN**, **USER TOKEN**)

    #time.sleep(3)

    checkHaleySMGStock('https://haleystrategic.com/shop/soft-goods/accessories/micro-smg-insert-black', "MINSERTSMG-BLK", **APPTOKEN**, **USER TOKEN**)

    time.sleep(3)

    checkTRexStock('https://www.trex-arms.com/store/t-rex-arms-orion/', **APPTOKEN**, **USER TOKEN**)

    time.sleep(3)

    listOfPreviousItems = checkCoyoteStock('http://www.coyotetacticalsolutions.com/pouches/', listOfPreviousItems, **APPTOKEN**, **USER TOKEN**)
    
    # Delay next try by pseudo-random time
    time.sleep(randDelay)
    #var = 0

print('Goodbye')
