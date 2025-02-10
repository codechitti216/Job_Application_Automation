from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time

# Load environment variables from .env file
load_dotenv("../config/.env")

LINKEDIN_EMAIL = os.getenv("LINKEDIN_EMAIL")
LINKEDIN_PASSWORD = os.getenv("LINKEDIN_PASSWORD")

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--disable-gpu")
chrome_options.add_experimental_option("detach", True)

# Initialize the WebDriver
driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)

try:
    # Open LinkedIn login page
    driver.get("https://www.linkedin.com/login")
    driver.maximize_window()
    time.sleep(2)

    # Enter credentials
    driver.find_element(By.ID, "username").send_keys(LINKEDIN_EMAIL)
    driver.find_element(By.ID, "password").send_keys(LINKEDIN_PASSWORD)
    driver.find_element(By.ID, "password").send_keys(Keys.RETURN)

    time.sleep(5)
    print("✅ Logged in successfully!")

    # Navigate to Jobs section
    driver.get("https://www.linkedin.com/jobs/")
    time.sleep(3)
    print("✅ Navigated to Jobs tab!")

    # Search for a job
    job_title = "Machine Learning Engineer"
    search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'jobs-search-box__text-input')]")))
    search_box.clear()
    search_box.send_keys(job_title)
    search_box.send_keys(Keys.RETURN)

    time.sleep(5)
    print(f"🔍 Searching for: {job_title}")

    # Get job results container
    job_results_container = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/div/div[2]/div[1]/div/ul')))
    job_elements = job_results_container.find_elements(By.XPATH, "./li")

    total_jobs = len(job_elements)
    print(f"✅ Found {total_jobs} job listings!")

    # Iterate through job listings and check for Easy Apply
    for i, job_element in enumerate(job_elements):
        try:
            job_link = job_element.find_element(By.TAG_NAME, "a")
            driver.execute_script("arguments[0].scrollIntoView();", job_link)
            job_link.click()
            time.sleep(3)

            # Get company name from right-side panel
            try:
                company_name = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[1]/div[1]/div/a")
                )).text.strip()
            except:
                company_name = "Unknown Company"

            # Get job title from right-side panel
            try:
                extracted_job_title = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[2]/div")
                )).text.strip()
            except:
                extracted_job_title = "Unknown Role"

            # Get job location from right-side panel
            try:
                location = wait.until(EC.presence_of_element_located(
                    (By.XPATH, "//*[@id='main']/div/div[2]/div[2]/div/div[2]/div/div/div[1]/div/div[1]/div/div[1]/div/div[3]/div/span[1]")
                )).text.strip()
            except:
                location = "Unknown Location"

            # Check for Easy Apply button
            try:
                driver.find_element(By.XPATH, "//button[contains(@class, 'jobs-apply-button') and contains(@aria-label, 'Easy Apply')]")
                easy_apply_status = "has an 'Easy Apply' option!"
            except:
                easy_apply_status = "does NOT have Easy Apply."

            print(f"{company_name} | {extracted_job_title} | {location} | {easy_apply_status}")

        except Exception as e:
            print(f"⚠️ Error on job {i+1}: {e}")

    print("✅ Completed job listings check!")

except Exception as e:
    print(f"❌ Error: {e}")

finally:
    input("Press Enter to close the browser...")
    driver.quit()
