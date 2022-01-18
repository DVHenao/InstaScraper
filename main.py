# Selenium imports here
import string
from typing import List, Any

from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# Other imports here
import os
import wget
import time
import csv

# baeutifulsoup imports
from bs4 import BeautifulSoup
import requests


# function definitions
def GatherLinks():
    print("a")


def Iteratelinks():
    print("a")


def Scroll():
    n_scrolls = 3
    for i in range(1, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


def LogIn():
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name= 'username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name= 'password']")))

    username.clear()
    password.clear()

    # username.send_keys("vrplayinbot")
    # password.send_keys("VRplay!n44")

    username.send_keys("introspectkid")
    password.send_keys("Natalia44~")

    log_in = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    not_now = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    not_now2 = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()


# variable initializations
followers = "0"
instafluencers: List[str] = []
insta_link = "https://www.instagram.com/"
hashtag = "torontoinfluencers"
list_final: List[any] = []

# INIT EXCEL
with open('mycsv.csv', 'w', newline='') as f:
    fieldnames = ['instagram name', 'real name', 'account style', 'followers']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

# writer.writerow(['instagram name', 'real name', 'account style', 'followers'])


# INIT BROWSER
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver: WebDriver = webdriver.Chrome(chrome_options=options,
                                     executable_path=r'C:/Users/Henao/Desktop/chrome driver/chromedriver.exe')
driver.get("https://www.instagram.com")

LogIn()

driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
time.sleep(1)

# START THE ITERATIONS
Scroll()

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')

links = [a['href'] for a in soup.find_all('a', href=True)]
for x in range(17):
    links.pop()

list_final = [insta_link + x for x in links]

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[1])

print(list_final)

for x in range(36):

    driver.get(list_final[x])
    time.sleep(1)

    url = driver.current_url
    url = url[:-15]
    driver.get(url)
    time.sleep(1)

    num = driver.find_elements(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/span")

    followers = num[0].text.replace(',', '').replace('k', '000').replace('.', '')

    if 15000 > int(followers) > 1000:
        insta_name = url[-26]
        real_name = driver.find_elements(By.XPATH, "//*[@id='react-root']/section/main/div/div[1]/h1")
        account_type = driver.find_elements(By.XPATH, "//*[@id='react-root']/section/main/div/div[1]/div/span")

        instafluencers.append(list_final[x])
    # writer.writerow({'instagram name': insta_name, 'real name': real_name[0].text,
    #                 'account style': account_type[0].text, 'followers': int(followers)})

        print(instafluencers)
        print(real_name[0].text)
        print(account_type[0].text)
