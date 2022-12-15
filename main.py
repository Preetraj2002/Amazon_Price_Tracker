import requests

from bs4 import BeautifulSoup

import smtplib
import os

product_url = input("Enter the product URL ")
target_price = int(input("Enter the target price: Rs."))  # use os env-var instead to fetch this data

body = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                  "Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7"
}

response = requests.get(url=product_url, headers=body)

website_content = response.text

soup = BeautifulSoup(website_content, "lxml")

product_title = soup.find(name="span", id="productTitle").getText().strip()
print(product_title)

price = soup.find(name="span", class_="a-price-whole").getText()
price1 = int(price.strip(".").replace(",", ""))

print(f"Price = Rs.{price1}")  # int
print(f"Target Price = Rs.{target_price}")

if price1 <= target_price:

    sender = os.environ["SMTP_sender"]
    receiver = os.environ["SMTP_receiver"]
    password = os.environ["SMTP_pass"]

    port_no = 587
    smtp_url = "smtp.gmail.com"

    mail = smtplib.SMTP(smtp_url, 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender, password)

    header = f"To:{receiver}\nSubject:Low Price Alert !!! on Amazon\n"
    content = f"The product that you were looking to buy is now at Rs.{price1} which is lower than your target price Rs.{target_price}.\n\n\n{product_title}\n\n\nGo buy it at \n\n{product_url}\n\n"
    message = header + content
    mail.sendmail(sender, receiver, message)
    mail.close()

else:
    print("Price is not lower than the target price.")
