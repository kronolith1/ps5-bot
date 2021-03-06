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


def check_for_stock():
    now = datetime.now()
    time = now.strftime("%H:%M:%S")

    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    #chrome_options.add_argument("--headless")
    chrome_options.add_experimental_option("prefs", {
        "profile.default_content_settings": {"images": 2},
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })

    driver = webdriver.Chrome(chrome_options=chrome_options)
    wait = WebDriverWait(driver, 20)

    driver.get("https://www.bol.com/nl/p/sony-playstation-5-console/9300000004162282/?ruleRedirect=1&sI=ps5&variants=") # PS5 URL
    driver.find_element_by_xpath("//*[@id='modalWindow']/div[2]/div[2]/wsp-consent-modal/div[2]/div/div[1]/button").click() # Accept cookies

    try:
        # If this element exists, the product is not in stock
        driver.find_element_by_class_name("buy-block__title")
        print(f"{time} - BOL.COM - NOT IN STOCK")
    except NoSuchElementException:
        print(f"{time} - BOL.COM - !! IN STOCK !! - Trying to order one for you, kind sir...")
        place_order(driver, wait)


def place_order(driver, wait):
    driver.find_element_by_class_name("js_btn_buy").click()
    
    # Add product to basket
    wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[4]/div[2]/div[3]/div[1]/div/div[2]/div/a")))
    driver.get("https://www.bol.com/nl/order/basket.html")

    wait.until(EC.element_to_be_clickable((By.ID, "continue_ordering_bottom")))
    driver.find_element_by_id("continue_ordering_bottom").click()

    # Login
    driver.execute_script("document.getElementById('login_email').value='.........'") #Bol username here
    driver.execute_script("document.getElementById('login_password').value='........'") #Bol password here
    
    time.sleep(2)

    driver.find_element_by_id("login_password").send_keys(Keys.ENTER)
    driver.find_element_by_xpath("//*[@id='executepayment']/form/div/button").click()

    print(f"{time} - BOL.COM - ORDER SUCCESFULLY PLACED")