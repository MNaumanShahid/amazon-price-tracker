import requests
from bs4 import BeautifulSoup
import pprint
import lxml
import smtplib
import os

PRODUCT_URL = "https://www.amazon.in/dp/B085SD9F3B/?th=1"
TARGET_PRICE = 400

FROM_ADR = os.environ.get("FROM_ADR")
PWD = os.environ.get("MAIL_PWD")
TO_ADR = os.environ.get("TO_ADR")

def send_email(message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=FROM_ADR, password=PWD)
        connection.sendmail(from_addr=FROM_ADR, to_addrs=TO_ADR, msg=message.encode('utf-8'))


headers = {
    "User-Agent": os.environ.get("USER_AGENT_CHROME"),
    "Accept-Language": os.environ.get("ACC_LANG")
}

response = requests.get(url=PRODUCT_URL, headers=headers)
webpage = response.text
soup = BeautifulSoup(webpage, 'lxml')

price = int(soup.find(name="span", class_="a-price-whole").getText().split(".")[0])
product_title = soup.find(name="span", id="productTitle").getText().strip()
# print(price)
# print(product_title)

if price < TARGET_PRICE:
    msg = f"Subject:Amazon Price Alert!\n\n{product_title} is now ₹{price}.\n" \
          f"{PRODUCT_URL}"
    send_email(message=msg)
else:
    print("Price is higher than target price.")