import re
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfeV1w9w1DOLgQ-UnWva2lyFn1J0CnJWtN-PUB9J7Od4l9e8w/viewform?usp=dialog"
response = requests.get(ZILLOW_URL)

# Get all the data from Zillow using BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

text_prices = soup.find_all(name="span", attrs={"data-test": "property-card-price"})
prices = [re.search(r"\$\d[\d,]*", price.text).group() for price in text_prices]


location_tag = soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor")
location_links = [location.get("href") for location in location_tag]


address_tag = soup.find_all(name="address", attrs={"data-test": "property-card-addr"})
addresses = [address.text.strip() for address in address_tag]


# Input and submit data found to google form
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

driver.get(GOOGLE_FORM_URL)
wait = WebDriverWait(driver, 10)

ADDRESS_XPATH = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
PRICE_XPATH = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
LINK_XPATH = '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
SUBMIT_XPATH = '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div'


for price, address, link in zip(prices, addresses, location_links):
    driver.get(GOOGLE_FORM_URL)

    # Wait and fill address
    address_input = wait.until(EC.element_to_be_clickable((By.XPATH, ADDRESS_XPATH)))
    address_input.send_keys(address)

    # Fill price
    price_input = wait.until(EC.element_to_be_clickable((By.XPATH, PRICE_XPATH)))
    price_input.send_keys(price)

    # Fill link (make sure it's full URL)
    full_link = link if link.startswith("http") else f"https://www.zillow.com{link}"
    link_input = wait.until(EC.element_to_be_clickable((By.XPATH, LINK_XPATH)))
    link_input.send_keys(full_link)

    # Submit
    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, SUBMIT_XPATH)))
    submit_button.click()

    # Optional: Wait before next submission
    time.sleep(1)

