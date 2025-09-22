import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

ACCOUNT_EMAIL = os.environ.get("DAY_50_TINDER_SWIPE_ACCOUNT_EMAIL")
ACCOUNT_PASSWORD = os.environ.get("DAY_50_TINDER_SWIPE_ACCOUNT_PASSWORD")
PHONE_NUMBER = os.environ.get("DAY_50_TINDER_SWIPE_PHONE_NUMBER")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(
    "https://tinder.com/app/recs"
)


def auto_dismiss_popup(driver, wait):
    try:
        print("🔍 Checking for 'Not interested' popup...")

        # Wait for the popup for up to 5 seconds
        popup_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[.//div[contains(text(), 'Not interested')]]")
            )
        )

        print("⚠️ Popup detected! Clicking 'Not interested'...")
        popup_button.click()

        # Optionally wait until it's gone
        wait.until(EC.invisibility_of_element_located(
            (By.XPATH, "//button[.//div[contains(text(), 'Not interested')]]")
        ))

        print("✅ Popup dismissed.")

    except TimeoutException:
        # No popup — proceed
        print("✅ No popup detected. Continuing...")


def safe_click(driver, element):
    try:
        element.click()
    except (ElementClickInterceptedException, ElementNotInteractableException):
        print("⚠️ Normal click failed — using JavaScript click.")
        driver.execute_script("arguments[0].click()", element)
    except Exception as e:
        print(f"❌ Unexpected error during click: {e}")


wait = WebDriverWait(driver, 10)

# Click login button
login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Log in']")))
safe_click(driver, login_button)

# Click login with Facebook
facebook_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[aria-label='Login with Facebook']")))
safe_click(driver, facebook_button)

# Wait for new window to appear
wait.until(lambda d: len(d.window_handles) > 1)

# Switch to the Facebook popup
driver.switch_to.window(driver.window_handles[1])

# Now try locating the input
input_email = wait.until(EC.element_to_be_clickable((By.ID, "email")))
input_email.send_keys(ACCOUNT_EMAIL)

input_password = wait.until(EC.element_to_be_clickable((By.ID, "pass")))
input_password.send_keys(ACCOUNT_PASSWORD)
input_password.send_keys(Keys.ENTER)

# Step 1: Manually log in
print("🔐 Please log in manually (Facebook, Google, phone number, etc.)")
print("✅ After you're fully logged in and see the Tinder swiping screen, press Enter here to continue...")
input("⏳ Waiting for manual login...")

# After Facebook login, switch back to the main Tinder window
for window in driver.window_handles:
    driver.switch_to.window(window)
    if "tinder.com" in driver.current_url:
        break

# Step 2: Start auto-swiping
print("🤖 Starting auto swiping...")
wait = WebDriverWait(driver, 10)

for i in range(20):  # Swipe 20 profiles
    try:
        auto_dismiss_popup(driver, wait)

        like_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[.//span[text()='Like']]")
        ))
        like_button.click()
        print(f"❤️ Swiped right on profile {i + 1}")
    except Exception as e:
        print(f"⚠️ Failed to swipe profile {i + 1}: {e}")
        time.sleep(3)
