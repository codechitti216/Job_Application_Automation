from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv("config/.env")

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")  
chrome_options.add_experimental_option("detach", True)

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)

# Open LinkedIn login page
driver.get("https://www.linkedin.com/login")
driver.maximize_window()
time.sleep(2)

# Enter credentials
driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

time.sleep(5)
print("Logged in successfully!")

input("Press Enter to close the browser...")
driver.quit()
