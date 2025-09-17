import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

ACCOUNT_EMAIL = "shin@test.com"
ACCOUNT_PASSWORD = "givemearandompassword12345"
GYM_URL = "https://appbrewery.github.io/gym/"

chrome_options = webdriver.ChromeOptions()
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")

# Chrome Options
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get(GYM_URL)
wait = WebDriverWait(driver, 10)


def retry(func, retries=5, description=""):
    """
    Retry a function multiple times before giving up.
    """
    for attempt in range(1, retries + 1):
        try:
            return func()
        except Exception as e:
            print(f"⚠️ Attempt {attempt}/{retries} failed for {description}: {e}")
            time.sleep(1)  # wait before retry
    raise Exception(f"❌ Failed after {retries} retries: {description}")


def login():
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-button")))
    login_button.click()

    email_input = wait.until(EC.presence_of_element_located((By.NAME, "email")))
    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))

    email_input.send_keys(ACCOUNT_EMAIL)
    password_input.send_keys(ACCOUNT_PASSWORD)

    submit_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[@type="submit"]')))
    submit_button.click()


def book_class(button, class_info, processed_classes):
    if button.text == "Booked":
        print(f"✓ Already booked: {class_info}")
        processed_classes.append(f"[Booked] {class_info}")
        return "already"
    elif button.text == "Waitlisted":
        print(f"✓ Already on waitlist: {class_info}")
        processed_classes.append(f"[Waitlisted] {class_info}")
        return "already"
    elif button.text == "Book Class":
        button.click()
        print(f"✓ Successfully booked: {class_info}")
        processed_classes.append(f"[New Booking] {class_info}")
        time.sleep(0.5)
        return "booked"
    elif button.text == "Join Waitlist":
        button.click()
        print(f"✓ Joined waitlist for: {class_info}")
        processed_classes.append(f"[New Waitlist] {class_info}")
        time.sleep(0.5)
        return "waitlist"
    else:
        raise Exception(f"Unexpected button text: {button.text}")


# Use retry wrapper for login
retry(login, retries=7, description="Login")

# Wait for schedule page to load
wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))

class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

booked_count = 0
waitlist_count = 0
already_booked_count = 0

# ----------------  Step 6: Book EVERY Tuesday AND Thursday 6pm class ----------------
# ----------------         and print a detailed class summary         ----------------

processed_classes = []

for card in class_cards:
    # Get the day title from the parent day group
    day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
    day_title = day_group.find_element(By.TAG_NAME, "h2").text

    if "Tue" in day_title or "Thu" in day_title:
        time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
        if "6:00 PM" in time_text:
            class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
            button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")

            # Track the class details
            class_info = f"{class_name} on {day_title}"

            result = retry(lambda: book_class(button, class_info, processed_classes),
                           description=f"Booking {class_info}")
            if result == "booked":
                booked_count += 1
            elif result == "waitlist":
                waitlist_count += 1
            elif result == "already":
                already_booked_count += 1

print("\n--- BOOKING SUMMARY ---")
print(f"New bookings: {booked_count}")
print(f"New waitlist entries: {waitlist_count}")
print(f"Already booked/waitlisted: {already_booked_count}")
print(f"Total Tuesday & Thursday 6pm classes: {booked_count + waitlist_count + already_booked_count}")

# Print detailed class list
print("\n--- DETAILED CLASS LIST ---")
for class_detail in processed_classes:
    print(f"  • {class_detail}")

# # ----------------  Step 7: Verify Class Bookings on My Bookings Page ----------------
#
# total_booked = already_booked_count + booked_count + waitlist_count
# print(f"\n--- Total Tuesday/Thursday 6pm classes: {total_booked} ---")
# print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")
#
# # Navigate to My Bookings page
# my_bookings_link = driver.find_element(By.ID, "my-bookings-link")
# my_bookings_link.click()
#
# # Wait for My Bookings page to load
# wait.until(EC.presence_of_element_located((By.ID, "my-bookings-page")))
#
# # Count all Tuesday/Thursday 6pm bookings
# verified_count = 0
#
# # Find ALL booking cards (both confirmed and waitlist)
# all_cards = driver.find_elements(By.CSS_SELECTOR, "div[id*='card-']")
#
# for card in all_cards:
#     try:
#         when_paragraph = card.find_element(By.XPATH, ".//p[strong[text()='When:']]")
#         when_text = when_paragraph.text
#
#         # Check if it's a Tuesday or Thursday 6pm class
#         if ("Tue" in when_text or "Thu" in when_text) and "6:00 PM" in when_text:
#             class_name = card.find_element(By.TAG_NAME, "h3").text
#             print(f"  ✓ Verified: {class_name}")
#             verified_count += 1
#     except NoSuchElementException:
#         # Skip if no "When:" text found (not a booking card)
#         pass
#
# # Simple comparison
# print(f"\n--- VERIFICATION RESULT ---")
# print(f"Expected: {total_booked} bookings")
# print(f"Found: {verified_count} bookings")
#
# if total_booked == verified_count:
#     print("✅ SUCCESS: All bookings verified!")
# else:
#     print(f"❌ MISMATCH: Missing {total_booked - verified_count} bookings")
