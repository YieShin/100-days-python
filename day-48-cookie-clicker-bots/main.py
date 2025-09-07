import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
# Don't use detach with undetected_chromedriver

driver = uc.Chrome(options=options)
driver.get("https://orteil.dashnet.org/cookieclicker/")

wait = WebDriverWait(driver, 10)
english_button = wait.until(EC.element_to_be_clickable((By.ID, "langSelect-EN")))
english_button.click()

# Wait for game to load UI
time.sleep(5)

cookie_button = wait.until(EC.element_to_be_clickable((By.ID, "bigCookie")))

# Run for 5 minutes
end_time = time.time() + 3000
next_check = time.time() + 5  # First check after 5 seconds

# Click the cookie until the time is up
while time.time() < end_time:
    cookie_button.click()

    # Every 5 seconds, check for upgrades and products
    if time.time() > next_check:
        # === Check for Upgrades ===
        upgrades = driver.find_elements(By.CSS_SELECTOR, "#upgrade0.enabled")
        if upgrades:
            upgrades[0].click()

        # === Check for Products ===
        product_ids = [f"product{i}" for i in range(20)]  # Check up to product19
        for pid in reversed(product_ids):  # Prioritize highest upgrade
            try:
                product = driver.find_element(By.ID, pid)
                if "enabled" in product.get_attribute("class"):
                    product.click()
                    break  # Only buy one product each check
            except:
                continue  # Ignore if not found

        next_check = time.time() + 5

# Keep the browser open for observation
time.sleep(9999)