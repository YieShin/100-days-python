import time
import os
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

PROMISED_DOWN = 100  # Your expected download speed (in Mbps)
PROMISED_UP = 10  # Your expected upload speed (in Mbps)
TWITTER_EMAIL = os.getenv("TWITTER_EMAIL")
TWITTER_PASSWORD = os.getenv("TWITTER_PASSWORD")


class InternetSpeedTwitterBot:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=chrome_options)
        self.down = 0
        self.up = 0
        self.wait = WebDriverWait(self.driver, 10)


    def get_internet_speed(self):
        try:
            self.driver.get("https://www.speedtest.net/")
            print("🕒 Navigated to Speedtest.net. Waiting for start button...")
            start_button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".start-text")))
            start_button.click()
            print("🚀 Started speed test. Waiting for result...")

            time.sleep(60)

            self.down = self.driver.find_element(By.CLASS_NAME, "download-speed").text
            self.up = self.driver.find_element(By.CLASS_NAME, "upload-speed").text
            print(f"✅ Download speed: {self.down} Mbps")
            print(f"✅ Upload speed: {self.up} Mbps")

            # Save speed_log to file (prepend new entry)
            timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            new_entry = f"Time: {timestamp}\nDownload: {self.down} Mbps\nUpload: {self.up} Mbps\n"

            try:
                with open("speed_log.txt", "r") as file:
                    old_content = file.read()
            except FileNotFoundError:
                old_content = ""

            with open("speed_log.txt", "w") as file:
                file.write(new_entry + "\n" + old_content)
        except Exception as e:
            print(f"❌ Error while testing speed: {e}")

    def tweet_at_provider(self):
        self.driver.get("https://x.com/")
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-testid='loginButton']")))
        login_button.click()

        if not TWITTER_EMAIL or not TWITTER_PASSWORD:
            raise ValueError("Missing TWITTER_EMAIL or TWITTER_PASSWORD environment variables.")

        email_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "text")))
        email_input.send_keys(TWITTER_EMAIL)
        email_input.send_keys(Keys.ENTER)

        pass_input = self.wait.until(EC.visibility_of_element_located((By.NAME, "password")))
        pass_input.send_keys(TWITTER_PASSWORD)
        pass_input.send_keys(Keys.ENTER)

        message = f"Hey Internet Provider, why is my internet speed {self.down}download/{self.up}upload when I pay for 300Mbps download"
        message_input = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div[aria-label='Post text']")))
        message_input.send_keys(message)

        post_button = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "//button[data-testid='tweetButtonInline']")))
        post_button.click()

bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()
