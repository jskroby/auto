import logging
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from modules.auth import login
from modules.scraper import update_profile
from modules.bot import send_telegram_message

# Configure Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def load_accounts():
    with open("config/accounts.json", "r") as file:
        return json.load(file)

def initialize_driver():
    """Initialize Selenium WebDriver"""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    
    try:
        driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        return driver
    except Exception as e:
        logging.error(f"Driver initialization failed: {e}")
        return None

def main():
    accounts = load_accounts()
    for account in accounts:
        driver = initialize_driver()
        if not driver:
            continue
        try:
            login(driver, account["email"], account["password"])
            update_profile(driver)
            send_telegram_message(f"✅ {account['email']} profile optimized successfully.")
        finally:
            driver.quit()

if __name__ == "__main__":
    main()
