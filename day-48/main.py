from selenium import webdriver
from selenium.webdriver.common.by import By

# Keep Chrome browser open after program finished

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.python.org/")

# price_dollar = driver.find_element(By.CLASS_NAME, "a-price-whole")
# price_cents = driver.find_element(By.CLASS_NAME, "a-price-fraction")
# print(f"The price is $ {price_dollar.text}.{price_cents.text}")

dates = driver.find_elements(By.CSS_SELECTOR, ".event-widget time")
titles = driver.find_elements(By.CSS_SELECTOR, ".event-widget li a")

# Build dictionary
events = {
    i: {"time": dates[i].text, "name": titles[i].text}
    for i in range(min(len(dates), len(titles)))
}

# Print result
for k, v in events.items():
    print(f"{k}: {v}")


driver.quit()

# driver.close() = close a tab
# driver.quit() = close entire browser


