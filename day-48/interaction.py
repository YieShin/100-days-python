from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://secure-retreat-92358.herokuapp.com/")

# article_count = driver.find_element(By.XPATH, '//*[@id="articlecount"]/ul/li[2]/a[1]')
# article_count.click()

# Find element by Link Text
# content_portals = driver.find_element(By.LINK_TEXT, "Content portals")
# content_portals.click()

# Find the "Search" <input> by Name
# search = driver.find_element(By.NAME, "search")

# Sending key input to Selenium
# search.send_keys("Python")
# search.send_keys(Keys.ENTER)

first_name = driver.find_element(By.NAME, "fName")
last_name = driver.find_element(By.NAME, "lName")
email = driver.find_element(By.NAME, "email")
submit = driver.find_element(By.XPATH, '/html/body/form/button')

first_name.send_keys("Yie")
last_name.send_keys("Shin")
email.send_keys("email@email.com")
submit.click()


