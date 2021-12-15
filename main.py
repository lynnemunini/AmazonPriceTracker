import requests
import lxml
import os
import smtplib
from bs4 import BeautifulSoup
import imghdr
from email.message import EmailMessage
from email.mime.text import MIMEText

target_price = 80.00
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")
URL = "https://www.amazon.com/Fitness-Tracker-Activity-Waterproof-Pedometer/dp/B09DG248ZY/ref=sr_1_4?" \
      "keywords=activity+tracker+and+smart+watches&pd_rd_r=375666cf-9968-464d-a1b4-1e4070b318f9&pd_rd_w=" \
      "9RRbP&pd_rd_wg=c9yBP&pf_rd_p=33f8f65b-b95c-44af-8b89-e59e69e79828&pf_rd_r=VG7DP8ESJZFS274GEJFV&qid=" \
      "1637061123&qsid=130-9493766-9488561&sr=8-4&sres=B08DKYLK4D%2CB09DG248ZY%2CB08DTF6YYD%2CB07TVC2KLW%2CB08HMRY8NG" \
      "%2CB074KBWL9J%2CB09K51GRMT%2CB08CHG524M%2CB084QB81LF%2CB087Q1WW12%2CB0925D4167%2CB094G2B1HW%2CB07Y4PT2NH%" \
      "2CB09F2RJCGD%2CB08MVR8LG9%2CB0823GXP3N&srpt=WEARABLE_COMPUTER"
user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36"
accept_language = "en-US,en;q=0.9"
headers = {
      "User-Agent": user_agent,
      "Accept-Language": accept_language
}
response = requests.get(URL, headers=headers)
webpage = response.text
soup = BeautifulSoup(webpage, "lxml")
# print(soup)
price_span = soup.find(name="span", class_="a-offscreen")
price = price_span.getText().split("$")[1]
price = float(price)
# print(price)

# Attach Picture
Sender_Email = os.environ.get("MY_EMAIL")
Reciever_Email = os.environ.get("TO")
Password = os.environ.get("PASSWORD")
newMessage = EmailMessage()
newMessage['Subject'] = "⌚AMAZON SMART WATCH PRICE ALERT!"
newMessage['From'] = os.environ.get("MY_EMAIL")
newMessage['To'] = os.environ.get("TO")
html = f"""\
<html>
  <body>
    <p>Only ${price} to get Smart Watch, D18S Fitness Tracker with Heart Rate Monitor, Activity Tracker with 1.44 Inch 
    Touch Screen, Waterproof, Sleep Monitor, Activity Tracker Pedometer for Women and Men.<br><br>
       <a href="https://www.amazon.com/Fitness-Tracker-Activity-Waterproof-Pedometer/dp/B09DG248ZY/ref=sr_1_4?
       keywords=activity+tracker+and+smart+watches&pd_rd_r=375666cf-9968-464d-a1b4-1e4070b318f9&pd_rd_w=9RRbP&pd_rd_wg=
       c9yBP&pf_rd_p=33f8f65b-b95c-44af-8b89-e59e69e79828&pf_rd_r=VG7DP8ESJZFS274GEJFV&qid=1637061123&qsid=
       130-9493766-9488561&sr=8-4&sres=B08DKYLK4D%2CB09DG248ZY%2CB08DTF6YYD%2CB07TVC2KLW%
       2CB08HMRY8NG%2CB074KBWL9J%2CB09K51GRMT%2CB08CHG524M%2CB084QB81LF%2CB087Q1WW12%2CB0925D4167%
       2CB094G2B1HW%2CB07Y4PT2NH%2CB09F2RJCGD%2CB08MVR8LG9%2CB0823GXP3N&srpt=WEARABLE_COMPUTER">Click here to purchase!
       </a> <br><br>
       Smart Watch Image Attached.
    </p>
  </body>
</html>
"""
newMessage.set_content(html, "html")
# newMessage.set_content(f'\n\nOnly ${price} to get Smart Watch, D18S Fitness Tracker with Heart Rate Monitor,  '
#                        f'Activity Tracker with 1.44 Inch Touch Screen, Waterproof, Sleep Monitor, Activity Tracker '
#                        f'Pedometer for Women and Men.\n\n\nSmart Watch Image attached!')
files = ['Smart Watch.jpg']

for file in files:
    with open(file, 'rb') as f:
        image_data = f.read()
        image_type = imghdr.what(f.name)
        image_name = f.name
    newMessage.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)


if price <= target_price:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password)
        smtp.send_message(newMessage)
