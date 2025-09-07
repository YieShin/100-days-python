from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_EMAIL = os.environ.get("ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.environ.get("ACCOUNT_PASSWORD")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(
    "https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491"
    "&keywords=python%20developer"
    "&location=London%2C%20England%2C%20United%20Kingdom"
    "&redirect=false&position=1&pageNum=0"
)

wait = WebDriverWait(driver, 10)


def safe_click(driver, element):
    try:
        element.click()
    except (ElementClickInterceptedException, ElementNotInteractableException):
        print("⚠️ Normal click failed — using JavaScript click.")
        driver.execute_script("arguments[0].click()", element)
    except Exception as e:
        print(f"❌ Unexpected error during click: {e}")


try:
    # Try modal button first
    signin_button = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, ".sign-in-modal")
    ))
    safe_click(driver, signin_button)
    time.sleep(1)

except (TimeoutException, NoSuchElementException, ElementClickInterceptedException) as e:
    print("Modal sign-in button not available. Trying fallback...")


# Wait for sign-in form to appear (this ensures inputs will be available)
MAX_RETRIES = 2
attempt = 0

while attempt < MAX_RETRIES:
    try:
        print(f"\n🔄 Attempt {attempt + 1} to find and fill sign-in form...")

        # Ensure the sign-in modal or form is present
        sign_in_form = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "form[data-id='sign-in-form']")
        ))
        print("✅ Sign-in form is present.")

        # Now ensure input fields are *visible* and interactable
        email_input = wait.until(EC.element_to_be_clickable((By.NAME, "session_key")))
        password_input = wait.until(EC.element_to_be_clickable((By.NAME, "session_password")))
        print("✅ Input fields are clickable.")

        # Fill and submit
        email_input.clear()
        password_input.clear()
        email_input.send_keys(ACCOUNT_EMAIL)
        password_input.send_keys(ACCOUNT_PASSWORD)
        password_input.send_keys(Keys.ENTER)

        print("🚀 Sign-in attempted successfully.")
        break  # done

    except (TimeoutException, NoSuchElementException, ElementNotInteractableException) as e:
        print(f"⚠️ Attempt {attempt + 1} failed: {e.__class__.__name__}")
        attempt += 1
        time.sleep(2)  # wait before retry

if attempt == MAX_RETRIES:
    print("❌ Gave up after multiple retries.")

# # Clicked on easy apply button
# easy_apply_button = wait.until(EC.element_to_be_clickable(
#     (By.CSS_SELECTOR, "button.jobs-apply-button")
# ))
# easy_apply_button.click()

# # Clicked on save job button
# job_save_button = wait.until(EC.element_to_be_clickable(
#     (By.CSS_SELECTOR, ".jobs-save-button")
# ))
# job_save_button.click()

# TODO Try to apply to all JOBS found