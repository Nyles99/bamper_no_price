import json
from turtle import pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import requests
from bs4 import BeautifulSoup
import os
import shutil
import csv
from PIL import Image, UnidentifiedImageError
import time


headers = {
    "Accept" : "application/json, text/javascript, */*; q=0.01",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
#options.add_experimental_option('useAutomationExtension', False)
options.add_argument('--ignore-certificate-errors')
options.add_argument("start-maximized") # // https://stackoverflow.com/a/26283818/1689770
options.add_argument("enable-automation")#  // https://stackoverflow.com/a/43840128/1689770
#options.add_argument("--headless")#  // only if you are ACTUALLY running headless
options.add_argument("--no-sandbox")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-dev-shm-usage")# //https://stackoverflow.com/a/50725918/1689770
options.add_argument("--disable-browser-side-navigation")# //https://stackoverflow.com/a/49123152/1689770
options.add_argument("--disable-gpu")
options.add_argument("--disable-infobars")# //https://stackoverflow.com/a/43840128/1689770
options.add_argument("--enable-javascript")

#options.add_argument("--proxy-server=31.204.2.182:9142")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})

summa = 0
black_list = []
black_mark = []
black_model = []

file1 = open("black-list.txt", "r")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_list.append(line)
#print(black_list)
# закрываем файл
file1.close

file1 = open("black-mark.txt", "r", encoding="utf-8")
while True:
    # считываем строку
    line = file1.readline()
    line = line.replace("\n","").replace("'","").replace(" ","")
    # прерываем цикл, если строка пустая
    if not line:
        break
    # выводим строку
    black_mark.append(line)
#print(black_list)

# закрываем файл
file1.close


"""url = "https://bamper.by/catalog/modeli/"

req = requests.get(url, headers=headers)
src = req.text
#print(src)
#with open("index.html", "w", encoding="utf-8") as file:
#    file.write(src)
#with open("index.html", encoding="utf-8") as file:
#    src = file.read()
soup = BeautifulSoup(src, 'html.parser')
#print(soup)
marka_need_list = {}
model_need_list = {}


all_mark_models = soup.find_all("h3", class_="title-2")
#print(all_mark_models)
for item in all_mark_models:
    item = str(item)
    item_text = item[item.find("gray")+6 : item.find("/h3")-6]
    item_href_marka = "https://bamper.by"+item[item.find("href=")+6 : item.find("style") - 2]
    #print(item_href_marka, item_text)
    if item_text not in black_mark:
        marka_need_list[item_text] = item_href_marka 
        

with open("marka.json", "a", encoding="utf-8") as file:
    json.dump(marka_need_list, file, indent=4, ensure_ascii=False)"""        

with open('marka.json', encoding="utf-8") as file:
    marka_need_list = json.load(file)

zapchast00_1200 = {}
zapchast1200 = {}
n=1

for item_text_marka, item_href_marka in marka_need_list.items():
    try:
        item_text = item_href_marka[32:len(item_href_marka)-1]
        print(item_text)    
        url_zapchast = f"https://bamper.by/zchbu/marka_{item_text}/god_2012-2024/price-do_0.5/isnew_y/?more=Y"
        #print(url_zapchast)
        driver.get(url=url_zapchast)
        time.sleep(1)

        with open(f"{item_text}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        with open(f"{item_text}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'html.parser')

        count = soup.find_all("h5", class_="list-title js-var_iCount")
        #print(count)
        for item in count:
            item = str(item)
            if "<b>" in item:
                #print(item)
                num_page = item[item.find("<b>")+3: item.find("</b>")]
                num_page = int(num_page.replace(" ",""))
                summa = summa + num_page
                if num_page > 0 and num_page < 1201:
                    page = int(num_page / 20) + 1
                    zapchast00_1200[url_zapchast] = page
                elif num_page > 1200:
                    page = int(num_page / 20) + 1
                    zapchast1200[url_zapchast] = page

        os.remove(f"{item_text}.html")
    except Exception:
        print("Ерунда какая-то")

    try:
        url_zapchast = f"https://bamper.by/zchbu/marka_{item_text}/god_2012-2024/price-do_0.5/isused_y/?more=Y"
        #print(url_zapchast)
        driver.get(url=url_zapchast)
        time.sleep(1)

        with open(f"{item_text}.html", "w", encoding="utf-8") as file:
            file.write(driver.page_source)

        with open(f"{item_text}.html", encoding="utf-8") as file:
            src = file.read()

        soup = BeautifulSoup(src, 'html.parser')

        count = soup.find_all("h5", class_="list-title js-var_iCount")
        #print(count)
        for item in count:
            item = str(item)
            if "<b>" in item:
                #print(item)
                num_page = item[item.find("<b>")+3: item.find("</b>")]
                num_page = int(num_page.replace(" ",""))
                summa = summa + num_page
                if num_page > 0 and num_page < 1201:
                    page = int(num_page / 20) + 1
                    zapchast00_1200[url_zapchast] = page
                elif num_page > 1200:
                    page = int(num_page / 20) + 1
                    zapchast1200[url_zapchast] = page

        os.remove(f"{item_text}.html")

    except Exception:
        print("Ерунда какая-то") 

with open("zapchast00_1200.json", "a", encoding="utf-8") as file:
    json.dump(zapchast00_1200, file, indent=4, ensure_ascii=False)

with open("zapchast1200.json", "a", encoding="utf-8") as file:
    json.dump(zapchast1200, file, indent=4, ensure_ascii=False)


print(summa)

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие ")