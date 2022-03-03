from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

options = webdriver.ChromeOptions()
options.add_argument('--incognito')

driverLocation = '/Users/gainwang/Downloads/chromedriver'

driver = webdriver.Chrome(driverLocation)
wait = WebDriverWait(driver, 10)

driver.get("https://www.etsy.com/signin")
username = driver.find_element_by_id("join_neu_email_field")
username.clear()
username.send_keys("USERNAME")

password = driver.find_element_by_id("join_neu_password_field")
password.clear()
password.send_keys("PASSWORD")

driver.find_element_by_name("submit_attempt").click()

driver.implicitly_wait(15)

wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='https://www.etsy.com/your/shops/me/dashboard?ref=hdr-mcpa']"))).click()

driver.find_element_by_xpath("//*[@id='root']/div/div[1]/div[3]/div/div[1]/div[2]/ul/li[5]/a/div/div[2]/span").click()

wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div/div[1]/div[3]/div/div[1]/div[2]/ul/li[5]/a/div/div[2]/span"))).click()

time.sleep(10)

ps = driver.page_source

soup = BeautifulSoup(ps, 'lxml')

info = []

time.sleep(5)

want = soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['float-left'])

for i in want:
    text = str(i.text)
    info.append(text)

items = {}

for i in range(len(info)):
  if "Quantity" in info[i]:
    """If item already exists in our dictionary"""
    if info[i+1][3:] in items:
      try:
        """Update existing quantity"""
        if "Color" in info[i+2]:
          items[info[i+1][3:]].update({info[i+2][5:]: items[info[i+1][3:]][info[i+2][5:]] + int(info[i][8:])})
        elif "Fabric" in info[i+2]:
          items[info[i+1][3:]].update({info[i+2][6:]: items[info[i+1][3:]][info[i+2][6:]] + int(info[i][8:])})
        elif "Size" in info[i+2]:
          items[info[i+1][3:]].update({info[i+2][4:]: items[info[i+1][3:]][info[i+2][4:]] + int(info[i][8:])})
        else:
          items[info[i+1][3:]].update({"Quantity": items[info[i+1][3:]][info[i+2][4:]] + int(info[i][8:])})
      except:
        pass
    else:
      try:
        if "Color" in info[i+2]:
          items[info[i+1][3:]] = {info[i+2][5:]: int(info[i][8:])}
        elif "Fabric" in info[i+2]:
          items[info[i+1][3:]] = {info[i+2][6:]: int(info[i][8:])}
        elif "Size" in info[i+2]:
          items[info[i+1][3:]] = {info[i+2][4:]: int(info[i][8:])}
        else:
          items[info[i+1][3:]] = {"Quantity": int(info[i][8:])}
      except:
        pass

print(items)
