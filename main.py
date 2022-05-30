# Selenium imports here
import csv
import time
from typing import List

# Other imports here
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# FIND A WAY INTO EXCEL WHERE
# I CAN ITERATE THROUGH ROWS UNTIL EMPTY AND THEN WRITE

# MAKE ITERATION TIME SMALLER BY SEPARATING INTO FUNCTIONS


# function definitions

def Excel1(listdata, csvTitle):
    # INIT EXCEL
    with open(csvTitle, 'w', newline='', encoding="utf-8") as f:
        fieldnames = ['instagram name', 'real name', 'account style', 'followers']
        writer = csv.writer(f)
        writer.writerow(fieldnames)
        print(listdata)
        writer.writerows(listdata)




def Scroll():
    n_scrolls = 4
    for i in range(1, n_scrolls):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)


def LogIn():
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name= 'username']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name= 'password']")))

    username.clear()
    password.clear()

    username.send_keys("vrplayinbot")
    password.send_keys("VRplay!n44")

    #username.send_keys("introspectkid")
    #password.send_keys("instagramNatalia44~")

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()


def IterationTime(iteration, data):
    failsave = 0  # failsave variable

    for x in range(iteration):

        # time.sleep(60) #timer to avoid block

        driver.switch_to.window(driver.window_handles[0])

        driver.get("https://www.instagram.com/explore/tags/" + data[x] + "/")
        time.sleep(60)

        Scroll()

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        print(soup)

        links = [a['href'] for a in soup.find_all('a', href=True)]
        for y in range(18):
            links.pop()

        print(links)

        links_final = [insta_link + x for x in links]

        driver.switch_to.window(driver.window_handles[1])

        for z in range(len(links_final)):  # len(links_final)

            driver.get(links_final[z])
            time.sleep(3)

            url = driver.current_url
            url = url[:-15]
            driver.get(url)
            time.sleep(3)

            num = driver.find_elements \
                (By.XPATH, "//*[@id='react-root']/section/main/div/header/section/ul/li[2]/a/div/span")

            if len(num) > 0:  # if num exists
                if num[0].text != 0:  # if num is not 0
                    if len(num[0].text) == 3:
                        followers = num[0].text.replace(',', '').replace('K', '000').replace('k', '000').replace('.', '').replace('m', '000000')
                    else:
                        followers = num[0].text.replace(',', '').replace('K', '00').replace('k', '00').replace('.', '').replace('m', '000000')

                # Criteria handling
                if 15000 > int(followers) > 900:

                    insta_name = url[26:]
                    hyperlink_name = '=HYPERLINK("' + url + '", "' + insta_name + '")'
                    real_name_element = driver.find_elements(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[2]/span")

                    account_type_element = driver.find_elements(By.XPATH, "//*[@id='react-root']/section/main/div/header/section/div[2]/div[1]/div")

                    if bool(account_type_element):
                        account_type = account_type_element[0].text
                    else:
                        account_type = "N/A"

                    if bool(real_name_element):
                        real_name = real_name_element[0].text
                    else:
                        real_name = "N/A"

                    data_final.append([hyperlink_name, real_name, account_type, followers])

            print(data_final)

            if len(num) == 0:  # counter if follower search failed
                print("failed")
                failsave += 1
            elif failsave != 0:  # search succeed and counter reset if need be
                failsave = 0

            if failsave == 5:  # exit function dues to repeating error
                # print("error occured 5 times, exiting function")
                print("error occured on iteration #" + str(x) + " and on links/list number #" + str(
                    z) + " (this is after 5 fails)")
                return


def CleanList(data):
    data_final_primary: List[any] = []
    data_final_secondary: List[any] = []

    print("begin cleaning")
    for elem in data:  # For Each list in list
        Business_flag = 0  # Bool for restricted accounts
        for value in elem:  # for each value within list of list
            if any(x in value.lower() for x in cleanout):  # if value matches any tag of restriction
                Business_flag = 1
        if Business_flag == 0:
            if elem not in data_final_secondary:  # if list value doesnt already exist

                data_final_secondary.append(elem)

    data_final_filtered = data_final_secondary
    print("clean version")
    print(data_final_filtered)

    Excel1(data_final_filtered, "mycsv.csv")

    # output_list = [item for items in data_final for item in items if search_string in item]


# variable initializations
insta_link = "https://www.instagram.com/"
hashtag = ["torontoinfluencer", "torontolife", "toronto", "torontostyle", "cntower", "nathanphilipssquare"]

hashtag3 =[ "torontofood", "torontoblogger", "todotoronto", "torontophotographer"]

hashtag4= ["downtowntoronto", "tastetoronto", "torontoeats", "torontocreator", "torontofashion",
            "torontoblogger", "yyzblogger", "torontofashionblogger"]

hashtag_test = ["tastetoronto"]

cleanout = ["restaurant", "store", "kitchen", "business", "fan page", "shop",
            "estate", "cafe", "eatery", "bakery", "pub", "bistro", "studio"
            "jewelry", "outlet", "company", "bar", "organization", "org",
            "retail", "agency", "fair", "event", "market", "buffet", "salon",
            "lease", "realtor", "broker", "lounge", "studio", "pizza", "cosmetic"
            "clinic", "service", "product", "legal", "school", "catering", "bank",
            "brand", "liquor", "delivery", "cosmetic", "capital", "wedding", "earrings",
            "clinic", "center", "hotel", "motel", "resort"]

followers = "0"
account_type = ""
real_name = ""
insta_name = ""
list_final: List[any] = []
data_final: List[any] = []
data_final_filtered: List[any] = []

# INIT BROWSER
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver: WebDriver = webdriver.Chrome(chrome_options=options,
                                     executable_path=r'C:\Users\User\Desktop\chrome webdriver/chromedriver.exe')
driver.get("https://www.instagram.com")

driver.execute_script("window.open('');")
driver.switch_to.window(driver.window_handles[0])

LogIn()
IterationTime(len(hashtag3), hashtag3)
CleanList(data_final)
