from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from datetime import datetime
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
import os.path
import telegram

# token generated with @BotFather and chatid of the 'bot' or 'group' on telegram
my_telegram_token = 'XXXX'
my_chatid = 'XXXX'
# iDeal bank, the below value must be present in your iDeal URL from your own bank.
my_bank = 'bunq'

def check_for_stock():
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")    
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_settings": {"images": 2},
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })

    driver = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.bol.com/nl/p/sony-playstation-5-console/9300000004162282/?ruleRedirect=1&sI=ps5&variants=")  # PS5 URL
    driver.find_element_by_xpath("//*[@id='modalWindow']/div[2]/div[2]/wsp-consent-modal/div[2]/div/div[1]/button").click()  # Accept cookies

    try:
        # If this element exists, the product is not in stock
        driver.find_element_by_class_name("buy-block__title")
        print(f"{time} - BOL.COM - NOT IN STOCK")
    except NoSuchElementException:
        print(f"{time} - BOL.COM - !! IN STOCK !! - Trying to order one for you, kind sir...")
        # Lets check if the file ordercompleted.txt is present to tell if we already ordered this product.
        if os.path.isfile('/app/persistent/ps5c-ordercompleted.txt'):
            print ("Order was already completed, no further action!")
        elif os.path.isfile('/app/persistent/ps5c-checkoutinprogress.txt'):
            print ("Checkout still in progress...")
        else:
            print ("No order was yet placed, proceeding to order...")
            place_order(driver, wait)

def place_order(driver, wait):
    # Create paymentfile to prevent multiple orders during checkout
    os.mknod("/app/persistent/ps5c-checkoutinprogress.txt")
    
    # Starting Checkout
    driver.find_element_by_class_name("js_btn_buy").click()

    # Add product to basket 
    time.sleep(1)
    driver.get("https://www.bol.com/nl/order/basket.html")

    wait.until(EC.element_to_be_clickable((By.ID, "continue_ordering_bottom")))
    driver.find_element_by_id("continue_ordering_bottom").click()
    print("Logging in...")

    # Login
    driver.execute_script("document.getElementById('login_email').value='XXXX'")  #Bol username here
    driver.execute_script("document.getElementById('login_password').value='XXXX'")  #Bol password here

    driver.find_element_by_id("login_password").send_keys(Keys.ENTER)
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='executepayment']/form/div/button").click()

    # Perform iDeal Payment - Must be set as default in your bol.com account and make sure your bank is also set as default!
    # Click the application button
    time.sleep(2)
    print("Sending iDeal to Telegram bot...")

    # Extract Payment URL
    requiredurl = driver.current_url
    paymentrequired = "Your BOT has prepared an order with BOL.com for the PS5 Disc Console - Please open the link and approve payment within 2 minutes - " + requiredurl
    sendtelegram(paymentrequired)

    # Check if we did make it to the iDeal page of the configured bank and create ordercompleted file if true
    createorderfile(requiredurl)
    
    # Wait for user to complete the payment
    print("Waiting for the user to complete payment...")
    time.sleep(120)

    # Create ordercompleted.txt file to tell the script the order has been placed
    
    print(f"{time} - BOL.COM - ORDER SUCCESFULLY PLACED")
    
    # Remove paymentfile to prevent multiple orders during checkout
    if os.path.exists("/app/persistent/ps5c-checkoutinprogress.txt"):
      os.remove("/app/persistent/ps5c-checkoutinprogress.txt")
    else:
      print("The payment file does not exist") 



def sendtelegram(msg, chat_id=my_chatid, token=my_telegram_token):
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    bot = telegram.Bot(token=token)
    bot.sendMessage(chat_id=chat_id, text=msg)

def createorderfile(requiredurl, bank=my_bank):
    """
    Create orderfile to make sure we do not buy this again.
    """
    if bank in requiredurl:
    	print(bank + " page found, creating file to prevent multiple buys")
    	os.mknod("/app/persistent/ps5c-ordercompleted.txt")
    else:
	print("Configured bank not found")
