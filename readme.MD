# PS5-bot

This bot checks stock availability on the PS5 for Bol.com every 2 seconds. When in stock, it will place an order.

# Dependencies

* NodeJS
* Selenium
* Telegram-bot
* Python 3
* Chrome + Chrome webdriver

# Installation

Just use the included `Dockerfile` to build a Docker image, it includes all necessary dependencies and is the easiest way to get up and running.
It is best to set persistent storage for container folder '/app/persistent/' so the check files created when completing an order will remain when the container is destroyed.

Don't want Docker? Install all external Python modules (`pip install -r requirements.txt`). Make sure to run `main.py` every x seconds. You will also need an up-to-date version of Chromedriver in your `PATH`.
