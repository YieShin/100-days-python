from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import smtplib

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
load_dotenv(dotenv_path=os.path.join(BASE_DIR, ".env"))

EMAIL_ADDRESS = os.getenv("DAY_47_LOWER_PRICE_SHOPPING_TO_EMAIL")
EMAIL_PASSWORD = os.getenv("DAY_47_LOWER_PRICE_SHOPPING_EMAIL_PASS")
TO_EMAIL = os.getenv("TO_EMAIL")

# url = "https://appbrewery.github.io/instant_pot/"
url = "https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/138.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",

           }
response = requests.get(url, headers)

soup = BeautifulSoup(response.text, "html.parser")
price = soup.find("span", class_="a-offscreen")
current_price = float(price.text.split("$")[1])
expected_price = 100

# Get the product title
title = soup.find(id="productTitle").get_text().strip()
short_title = " ".join(title.split()[:5])

if current_price < expected_price:
    # Email setup
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = TO_EMAIL
    msg['Subject'] = f"{title} is on sale for {current_price}!"

    # Email body (HTML format)
    body = f"""
    <p><strong>{title}</strong> is now <strong>RM{current_price}</strong>, lower than expected RM{expected_price}!</p>
    <p>Click <a href="{url}">here</a> to check the product.</p>
    """

    msg.attach(MIMEText(body, "html", "utf-8"))

    # # Send email
    # try:
    #     with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    #         smtp.ehlo()
    #         smtp.starttls()
    #         smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    #         smtp.sendmail(EMAIL_ADDRESS, TO_EMAIL, msg.as_string())
    #         print("✅ Email sent successfully!")
    # except Exception as e:
    #     print(f"❌ Error sending email: {e}")
else:
    print("Still above 100")
#
#
