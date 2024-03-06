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

#options.add_argument("--proxy-server=188.119.120.29:54375")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    'source': '''
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise:
        delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol:
    '''
})

summa = 0

driver.get(url="https://bamper.by/catalog/modeli/")
time.sleep(30)

zapchast00_1200_year_price_one_year = {}
zapchast1200_year_price_one_year = {}
null_or_xz = {}

with open("zapchast1200.json", encoding="utf-8") as file:
    srazy_parsim = json.load(file)


#"https://bamper.by/zchbu/marka_skoda/god_2012-2024/price-do_0.5/isused_y/?more=Y"

for item_href_categories, count_page in srazy_parsim.items():
    if count_page > 1:
        href_zapchast = []
        item_href_categories = str(item_href_categories)
        first_part = item_href_categories[ : item_href_categories.find("god_")+ 4]
        second_part = item_href_categories[item_href_categories.find("/price-do_") : ]
        for year in range(2012, 2025):
            url_zapchast = f"{first_part}{year}-{year}{second_part}"
            
            print(url_zapchast)
            try:
            #print(url_zapchast)
                driver.get(url=url_zapchast)
                time.sleep(1)

                with open("excample.html", "w", encoding="utf-8") as file:
                    file.write(driver.page_source)

                with open("excample.html", encoding="utf-8") as file:
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
                        print(num_page)
                        summa = summa + num_page
                        if num_page > 0 and num_page < 1201:
                            page = int(num_page / 20) + 1
                            zapchast00_1200_year_price_one_year[url_zapchast] = page
                        elif num_page > 1200:
                            page = int(num_page / 20) + 1
                            zapchast1200_year_price_one_year[url_zapchast] = page
                        elif num_page == 0:
                            print(url_zapchast, "Страница с нулевым значением нам не нужна")
                        else:
                            null_or_xz[url_zapchast] = page
                            print("Страница записалась в отдельный список")

                os.remove("excample.html")
            except Exception:
                null_or_xz[url_zapchast] = count_page
                print(f"Не загрузилась {url_zapchast} - загрузим позже, попробуй обновить вручную в браузере")   

with open("zapchast00_1200_one_year.json", "a", encoding="utf-8") as file:
    json.dump(zapchast00_1200_year_price_one_year, file, indent=4, ensure_ascii=False)

with open("zapchast1200_one_year.json", "a", encoding="utf-8") as file:
    json.dump(zapchast1200_year_price_one_year, file, indent=4, ensure_ascii=False)

with open("null.json", "a", encoding="utf-8") as file:
    json.dump(null_or_xz, file, indent=4, ensure_ascii=False)


print(summa)

a = input("Нажмите 1 и ENTER, чтобы закончить это сумасшествие")