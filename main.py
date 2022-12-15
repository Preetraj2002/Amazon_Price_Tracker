import requests

from bs4 import BeautifulSoup

import smtplib
import os


target_price=1500


product_url="https://www.amazon.in/KENT-Electric-Steamer-Vegetables-Stainless/dp/B0B5KZ3C53/ref=sr_1_1_sspa?crid" \
            "=8A9AD5AVSB3C&keywords=electric+cooker&qid=1671106569&sprefix=electric+cooke%2Caps%2C331&sr=8-1-spons" \
            "&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1 "
body={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 "
                 "Safari/537.36",
    "Accept-Language":"en-GB,en-US;q=0.9,en;q=0.8,bn;q=0.7"
}

response=requests.get(url=product_url,headers=body)
# pprint(response.text)
website_content=response.text

soup=BeautifulSoup(website_content,"lxml")
# print(soup.prettify())
# title_tag=soup.find_all(name="title")
# print(title_tag)

product_title=soup.find(name="span",id="productTitle").getText().strip()
print(product_title)

price=soup.find(name="span",class_="a-price-whole").getText()
price1=int(price.strip(".").replace(",",""))
# print(price)
print(f"Price = Rs.{price1}")       #int
print(f"Target Price = Rs.{target_price}")


if price1 <= target_price:

    sender=os.environ["SMTP_sender"]
    receiver=os.environ["SMTP_receiver"]
    password1=os.environ["SMTP_pass"]
    password="wtaspagofkqxtxer"


    port_no=587
    smtp_url= "smtp.gmail.com"

    mail=smtplib.SMTP(smtp_url, 587)
    mail.ehlo()
    mail.starttls()
    mail.login(sender,password)

    header=f"To:{receiver}\nSubject:Low Price Alert !!! on Amazon\n"
    content=f"The product that you were looking to buy is now at Rs.{price1} which is lower than your target price Rs.{target_price}.\n\n\n{product_title}\n\n\nGo buy it at \n\n{product_url}\n\n"
    message=header+content
    mail.sendmail(sender,receiver,message)
    mail.close()

else:
     print("Price is not lower than the target price.")
