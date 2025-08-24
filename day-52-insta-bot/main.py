from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 👉 Set your custom user data directory path
USER_DATA_DIR = "/Users/yieshin/Documents/selenium_profile"

chrome_options = Options()
chrome_options.add_argument(f"--user-data-dir={USER_DATA_DIR}")
chrome_options.add_argument("--profile-directory=Default")  # optional

# Optional: Keep browser open after script ends
chrome_options.add_experimental_option("detach", True)

# Create driver
driver = webdriver.Chrome(options=chrome_options)

# ✅ Go to Instagram (or any site you want to stay logged into)
driver.get("https://www.instagram.com/")

# ⏱️ Give yourself time to manually log in (only once)
time.sleep(60)
