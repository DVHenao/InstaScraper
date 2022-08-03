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

    #vrplayinbotmom@gmail.com
    #username.send_keys("vrplayinbotmom")
    #password.send_keys("VRplay!n")

    username.send_keys("vrplayinbot")
    password.send_keys("VRplay!n44")

    #username.send_keys("introspectkid")
    #password.send_keys("instaNatalia44~")

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

        driver.get("https://www.instagram.com/explore/" + data[x] + "/")
        time.sleep(5)

        Scroll()

        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        links = [a['href'] for a in soup.find_all('a', href=True)]
        for y in range(18):
            links.pop()

        print(links)

        links_final = [insta_link + x for x in links]

        driver.switch_to.window(driver.window_handles[1])


        for z in range(len(links_final)):  # len(links_final)

            driver.get(links_final[z])
            #driver.get("https://www.instagram.com/p/CeXa4bzsbGE")
            time.sleep(5)

            page_not_found = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/div/div/h2')
            if page_not_found:
                if page_not_found[0].text == "Sorry, this page isn't available":
                    continue
            else:
                account_url = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div[1]/div/div/span/a')
                if not account_url:
                    account_url = driver.find_elements(By.XPATH, '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div[1]/div[1]/article/div/div[2]/div/div[1]/div/header/div[2]/div[1]/div/div/span[1]/a')
                url = "https://www.instagram.com/" + account_url[0].text
                driver.get(url)
                time.sleep(5)

                num = driver.find_elements(By.XPATH,
                                           '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span')

                if len(num) > 0:  # if num exists
                    if num[0].text != 0:  # if num is not 0
                        if len(num[0].text) == 3:
                            followers = num[0].text.replace(',', '').replace('K', '000').replace('k', '000').replace('.',
                                                                                                                     '').replace(
                                'm', '000000')
                        else:
                            followers = num[0].text.replace(',', '').replace('K', '00').replace('k', '00').replace('.',
                                                                                                                   '').replace(
                                'm', '000000')

                    # Criteria handling
                    if 15000 > int(followers) > 900:

                        insta_name = url[26:]
                        hyperlink_name = '=HYPERLINK("' + url + '", "' + insta_name + '")'
                        real_name_element = driver.find_elements(By.XPATH,
                                                                 '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/div[3]/span')

                        account_type_element = driver.find_elements(By.XPATH,
                                                                    '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/div[3]/div[1]/div')

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
hashtag = ["tags/torontoinfluencer", "tags/toronto", "tags/torontostyle", "tags/cntower", "tags/nathanphilipssquare"]

hashtag2 = ["tags/torontofood", "tags/torontoblogger", "tags/todotoronto", "tags/torontophotographer", "tags/torontolife"]

hashtag3 = ["tags/downtowntoronto", "tags/tastetoronto", "tags/torontoeats", "tags/torontocreator", "tags/torontofashion",
            "tags/torontoblogger", "tags/yyzblogger", "tags/torontofashionblogger"]

locations = ["locations/213307564/cf-toronto-eaton-centre", "locations/219374409/kensington-market",
             "locations/217007065/bloor-west-village", "locations/766599654/harbourfront",
             "locations/1024105922/yorkdale/" ]

locations2 = ["locations/6292856/high-park-nature-centre/", "locations/213376054/cn-tower-tour-cn/",
             "locations/213376054/cn-tower-tour-cn/", "locations/213492097/ago-art-gallery-of-ontario/",
             "locations/754713159/toronto-science-center/" ]

locations3 = ["locations/735793648/casa-loma/", "locations/316318748/danforth-greek-town/",
             "locations/974997839/toronto-convention-center/", "locations/140286933299523/toronto-reference-library/",
             "locations/243699149/ryerson-university-young-dundas/", "locations/55855/university-of-toronto/" ]


hashtag_test = ["tastetoronto"]

cleanout = ["restaurant", "store", "kitchen", "business", "fan page", "shop",
            "estate", "cafe", "eatery", "bakery", "pub", "bistro", "studio"
                                                                   "jewelry", "outlet", "company", "bar",
            "organization", "org",
            "retail", "agency", "fair", "event", "market", "buffet", "salon",
            "lease", "realtor", "broker", "lounge", "studio", "pizza", "cosmetic"
                                                                       "clinic", "service", "product", "legal",
            "school", "catering", "bank",
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
IterationTime(len(hashtag2), hashtag2)

#datatemp = [['=HYPERLINK("https://www.instagram.com/tolulopesolutions", "tolulopesolutions")', 'Tolulope Adejumo | Lifestyle Blogger', 'Digital creator', '12600'], ['=HYPERLINK("https://www.instagram.com/itsjimzen", "itsjimzen")', 'jimzen', 'Personal blog', '2320'], ['=HYPERLINK("https://www.instagram.com/mikerizzi", "mikerizzi")', 'MICHAEL RIZZI', 'Video creator', '13100'], ['=HYPERLINK("https://www.instagram.com/baahar.k", "baahar.k")', 'Baahar K', 'N/A', '4567'], ['=HYPERLINK("https://www.instagram.com/twinmamaslife", "twinmamaslife")', 'Mehwish || YYZ Blogger 🇨🇦', 'Digital creator', '14300'], ['=HYPERLINK("https://www.instagram.com/christianelinee", "christianelinee")', 'C H R I S T I A N E', 'Digital creator', '13100'], ['=HYPERLINK("https://www.instagram.com/abinaartistry", "abinaartistry")', 'A B I N A • A R T I S T R Y', 'Digital creator', '2120'], ['=HYPERLINK("https://www.instagram.com/enfancebaby", "enfancebaby")', 'Enfance Baby & Kids Store', "Baby & children's clothing store", '1599'], ['=HYPERLINK("https://www.instagram.com/mandrcustomproducts", "mandrcustomproducts")', 'M&R Custom Products', 'Business service', '4785'], ['=HYPERLINK("https://www.instagram.com/becca.ebs", "becca.ebs")', 'REBECCA EBSWORTHY', 'N/A', '3224'], ['=HYPERLINK("https://www.instagram.com/stylewithayla", "stylewithayla")', 'ayla 🕊 | Fashion + Lifestyle', 'Digital creator', '1546'], ['=HYPERLINK("https://www.instagram.com/wellthybyjess", "wellthybyjess")', 'jessica koper', 'Digital creator', '6620'], ['=HYPERLINK("https://www.instagram.com/publicistgroup", "publicistgroup")', 'THE PUBLICIST GROUP', 'N/A', '3913'], ['=HYPERLINK("https://www.instagram.com/chapters_of_katie", "chapters_of_katie")', 'Katie| Vintage& cottagecore', 'Personal blog', '12400'], ['=HYPERLINK("https://www.instagram.com/looksby_leigh", "looksby_leigh")', 'LEIGH ALEXANDRA', 'Digital creator', '3191'], ['=HYPERLINK("https://www.instagram.com/s.jdk17", "s.jdk17")', 'ⓢ 🕊 Content/UGC Creator + Model', 'Digital creator', '4874'], ['=HYPERLINK("https://www.instagram.com/thekarinasmith", "thekarinasmith")', 'Karina Toronto, Canada blogger', 'N/A', '9874'], ['=HYPERLINK("https://www.instagram.com/princesspeaboutique", "princesspeaboutique")', 'Princess and the Pea Boutique', 'Product/service', '1503'], ['=HYPERLINK("https://www.instagram.com/superherofoodies", "superherofoodies")', '🦸🏾\u200d♀️🅡🅘🅒🅐 & 🦸🏿\u200d♂️🅚🅔🅥🅘🅝', 'N/A', '4848'], ['=HYPERLINK("https://www.instagram.com/highwaysnrunways", "highwaysnrunways")', 'Sudi | Travel | Canada |', 'N/A', '5663'], ['=HYPERLINK("https://www.instagram.com/mandrcustomproducts", "mandrcustomproducts")', 'M&R Custom Products', 'Business service', '4785'], ['=HYPERLINK("https://www.instagram.com/abiradcliffe_", "abiradcliffe_")', 'Abi Radcliffe', 'Digital creator', '6360'], ['=HYPERLINK("https://www.instagram.com/pooja_bliss", "pooja_bliss")', 'Pooja Panda', 'Blogger', '6079'], ['=HYPERLINK("https://www.instagram.com/thatbrowngirlllllll", "thatbrowngirlllllll")', 'Simran 🦄', 'Movie Character', '4302'], ['=HYPERLINK("https://www.instagram.com/christianelinee", "christianelinee")', 'C H R I S T I A N E', 'Digital creator', '13100'], ['=HYPERLINK("https://www.instagram.com/nicolemiasik", "nicolemiasik")', 'nicole', 'Fashion Model', '999'], ['=HYPERLINK("https://www.instagram.com/thelandofdustin", "thelandofdustin")', 'Dustin', 'Photographer', '12900'], ['=HYPERLINK("https://www.instagram.com/digigraphs", "digigraphs")', 'Mohsen M', 'Photographer', '3189'], ['=HYPERLINK("https://www.instagram.com/sukhbasran", "sukhbasran")', 'Sukhmani Basran', 'N/A', '7091'], ['=HYPERLINK("https://www.instagram.com/alexis.d", "alexis.d")', 'lex', 'N/A', '6902'], ['=HYPERLINK("https://www.instagram.com/chimeracollectiongta", "chimeracollectiongta")', 'N/A', 'Boutique Store', '1041'], ['=HYPERLINK("https://www.instagram.com/chrisoliverrealestate", "chrisoliverrealestate")', 'Chris Oliver Real Estate', 'Real Estate Agent', '3121'], ['=HYPERLINK("https://www.instagram.com/soundofpayal", "soundofpayal")', 'PAYAL', 'Digital creator', '6129'], ['=HYPERLINK("https://www.instagram.com/faultylogikstudios", "faultylogikstudios")', 'YORK REGION CREATIVE SPACE', 'Photography Videography', '1870'], ['=HYPERLINK("https://www.instagram.com/jennifervansickleteam", "jennifervansickleteam")', 'The Jennifer Van Sickle Team', 'Real Estate', '2792'], ['=HYPERLINK("https://www.instagram.com/brokenfilter", "brokenfilter")', 'Jae R HAIRSTYLIST/ WIG MAKER', 'N/A', '1755'], ['=HYPERLINK("https://www.instagram.com/pc275", "pc275")', 'PC275 Toronto | London | Woodstock | Sarnia | Ontario', 'Real Estate Service', '1502'], ['=HYPERLINK("https://www.instagram.com/sweetbrucardz", "sweetbrucardz")', 'CEO《VAUGHAN CON》💎 SQUAD', 'N/A', '5141'], ['=HYPERLINK("https://www.instagram.com/fairviewchrysler", "fairviewchrysler")', 'Fairview Chrysler', 'Car dealership', '1818'], ['=HYPERLINK("https://www.instagram.com/sammyhuynn", "sammyhuynn")', 'Sammy | Sustainable Style', 'N/A', '9961'], ['=HYPERLINK("https://www.instagram.com/shopthepinkdoor_to", "shopthepinkdoor_to")', 'Toronto Clothing Boutiques', 'N/A', '4937'], ['=HYPERLINK("https://www.instagram.com/alanapancyr", "alanapancyr")', 'Alana Pancyr', 'Actor', '11100'], ['=HYPERLINK("https://www.instagram.com/lolageorgesss", "lolageorgesss")', 'Lola', 'N/A', '6572'], ['=HYPERLINK("https://www.instagram.com/finermomentscatalogue", "finermomentscatalogue")', 'Aesthetics•Outfits•Lifestyle', 'Blogger', '2137'], ['=HYPERLINK("https://www.instagram.com/luckshene", "luckshene")', '𝐋𝐮𝐜𝐤𝐲 | 𝐨𝐮𝐭𝐟𝐢𝐭 𝐢𝐧𝐬𝐩𝐨', 'Digital creator', '7745'], ['=HYPERLINK("https://www.instagram.com/myloupolman", "myloupolman")', 'Mylou', 'Personal blog', '7144'], ['=HYPERLINK("https://www.instagram.com/trukimmy", "trukimmy")', 'Kimberly-Ann Trương', 'N/A', '4425'], ['=HYPERLINK("https://www.instagram.com/blackandwhiteremix", "blackandwhiteremix")', 'Official Black&White REMIX', 'Public figure', '14600'], ['=HYPERLINK("https://www.instagram.com/assinewejewelry", "assinewejewelry")', 'Assinewe Jewelry', 'Shopping & retail', '12800'], ['=HYPERLINK("https://www.instagram.com/platosclosetmarkham", "platosclosetmarkham")', 'ℙ𝕝𝕒𝕥𝕠𝕤 ℂ𝕝𝕠𝕤𝕖𝕥 𝕄𝕒𝕣𝕜𝕙𝕒𝕞', 'Thrift & Consignment Store', '3985'], ['=HYPERLINK("https://www.instagram.com/keetz_ana", "keetz_ana")', 'k e e t z _ a n a', 'Personal blog', '1731'], ['=HYPERLINK("https://www.instagram.com/martametyk", "martametyk")', 'Marta Metyk - UA fashion in TO', 'Accessories', '5512'], ['=HYPERLINK("https://www.instagram.com/martametyk", "martametyk")', 'Marta Metyk - UA fashion in TO', 'Accessories', '5512'], ['=HYPERLINK("https://www.instagram.com/rachelsavaunnah", "rachelsavaunnah")', 'RAE • TORONTO CREATOR', 'Digital creator', '11800'], ['=HYPERLINK("https://www.instagram.com/kaltenbock", "kaltenbock")', 'Kaltenbock Opticians', 'N/A', '1391'], ['=HYPERLINK("https://www.instagram.com/yokafashions", "yokafashions")', 'Yoka', 'Shopping & retail', '8460'], ['=HYPERLINK("https://www.instagram.com/teamsoldtoday", "teamsoldtoday")', 'Team SoldToday', 'Real Estate', '1587'], ['=HYPERLINK("https://www.instagram.com/claw.xx", "claw.xx")', 'Claudia', 'N/A', '915'], ['=HYPERLINK("https://www.instagram.com/claw.xx", "claw.xx")', 'Claudia', 'N/A', '915'], ['=HYPERLINK("https://www.instagram.com/revelleshop", "revelleshop")', 'Revelle', "Women's clothing store", '7043'], ['=HYPERLINK("https://www.instagram.com/royalstone.ca", "royalstone.ca")', 'Royal Stone Landscaping', 'Landscape Company', '13500'], ['=HYPERLINK("https://www.instagram.com/vukswim", "vukswim")', 'VUK - Sustainable Swimwear', 'Entrepreneur', '1807'], ['=HYPERLINK("https://www.instagram.com/josh__wray", "josh__wray")', 'Josh Cowling', 'N/A', '1855'], ['=HYPERLINK("https://www.instagram.com/ohh.miaa", "ohh.miaa")', 'Mia | Fashion Inspo', 'Digital creator', '14300'], ['=HYPERLINK("https://www.instagram.com/ilknuraydeniz_", "ilknuraydeniz_")', 'Ilknur', 'Digital creator', '14000'], ['=HYPERLINK("https://www.instagram.com/_ashleychung", "_ashleychung")', 'Ashley ᵕ̈', 'Digital creator', '2975'], ['=HYPERLINK("https://www.instagram.com/thelandofdustin", "thelandofdustin")', 'Dustin', 'Photographer', '12900'], ['=HYPERLINK("https://www.instagram.com/soyjossmolina", "soyjossmolina")', 'N/A', 'N/A', '6610'], ['=HYPERLINK("https://www.instagram.com/chicago_ryan", "chicago_ryan")', '🌹 Ryan まさあき', 'N/A', '10300'], ['=HYPERLINK("https://www.instagram.com/juliancompton", "juliancompton")', 'Julian Compton', 'N/A', '3677'], ['=HYPERLINK("https://www.instagram.com/goodtimesgta", "goodtimesgta")', 'Good Times GTA', 'Media/news company', '2144'], ['=HYPERLINK("https://www.instagram.com/jaskaran_dhaliwl", "jaskaran_dhaliwl")', 'Jassa Dhaliwal', 'Artist', '1673'], ['=HYPERLINK("https://www.instagram.com/pameangel", "pameangel")', 'Pamela Angel♛', 'Photographer', '1446'], ['=HYPERLINK("https://www.instagram.com/pamela4xx", "pamela4xx")', 'Pamela4xx', 'N/A', '1301'], ['=HYPERLINK("https://www.instagram.com/misaelescoto", "misaelescoto")', 'Misael Escoto', 'N/A', '2774'], ['=HYPERLINK("https://www.instagram.com/dsslight", "dsslight")', 'Diana \U0001faf6🏾', 'Personal blog', '4175'], ['=HYPERLINK("https://www.instagram.com/kazikreg", "kazikreg")', 'Kazi, Realtor ®', 'Real Estate Agent', '1277'], ['=HYPERLINK("https://www.instagram.com/argenel", "argenel")', 'Argen Elezi', 'Photographer', '13800'], ['=HYPERLINK("https://www.instagram.com/naisargisheth", "naisargisheth")', 'Naisargi Sheth♥️', 'Personal blog', '3058'], ['=HYPERLINK("https://www.instagram.com/ble55ed_f97", "ble55ed_f97")', '🏎 tdot/yeg 🇨🇦', 'N/A', '3159'], ['=HYPERLINK("https://www.instagram.com/wealth_madison", "wealth_madison")', 'caleb madison', 'N/A', '1285'], ['=HYPERLINK("https://www.instagram.com/guycalledalex", "guycalledalex")', 'Alex Perkes', 'N/A', '1472'], ['=HYPERLINK("https://www.instagram.com/oft_geflogen_tief_gefallen", "oft_geflogen_tief_gefallen")', 'Adam', 'N/A', '961'], ['=HYPERLINK("https://www.instagram.com/balancebarbershop", "balancebarbershop")', 'Balance Barbershop', 'N/A', '1223'], ['=HYPERLINK("https://www.instagram.com/infectious_travels08", "infectious_travels08")', '🌎 Infectious Travels 🌍', 'Personal blog', '3184'], ['=HYPERLINK("https://www.instagram.com/nateharijanto", "nateharijanto")', 'Nate Harijanto', 'N/A', '993'], ['=HYPERLINK("https://www.instagram.com/sweetpsychosarah", "sweetpsychosarah")', 'Sarah Francis Gallagher', 'N/A', '1853'], ['=HYPERLINK("https://www.instagram.com/ajay_kartha", "ajay_kartha")', 'Ajaykumar', 'Photographer', '1011'], ['=HYPERLINK("https://www.instagram.com/pav_lifestyle", "pav_lifestyle")', 'Pav', 'Personal blog', '12600'], ['=HYPERLINK("https://www.instagram.com/booboobabygurl", "booboobabygurl")', 'Jessica Burstoff Meunier', 'N/A', '2392'], ['=HYPERLINK("https://www.instagram.com/johnnotten", "johnnotten")', 'John Notten', 'N/A', '1033'], ['=HYPERLINK("https://www.instagram.com/vimac_photos", "vimac_photos")', 'Vito Macri', 'N/A', '1216'], ['=HYPERLINK("https://www.instagram.com/crateddozen", "crateddozen")', 'Jason Egbuna', 'Photographer', '3424'], ['=HYPERLINK("https://www.instagram.com/josephyossi", "josephyossi")', "Joseph's Lens", 'Photographer', '1969'], ['=HYPERLINK("https://www.instagram.com/hanne_h_sten", "hanne_h_sten")', 'Hanne Sten', 'N/A', '1174'], ['=HYPERLINK("https://www.instagram.com/hrvemusic", "hrvemusic")', 'HRVE', 'Artist', '4668'], ['=HYPERLINK("https://www.instagram.com/events2life", "events2life")', 'Events2Life', 'N/A', '4434']]

CleanList(data_final)
