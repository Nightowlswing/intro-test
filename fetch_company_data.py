
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from os import path
from os import listdir
from parse_data import update_and_save
from parse_data import save_news
import pathlib
import time

current_dir = str(pathlib.Path().absolute())
options = Options()


#Prefs for chromedriver for downloading files
PREFS = {
  "download.default_directory": current_dir,
  "download.prompt_for_download": False,
  "download.directory_upgrade": True,
  "safebrowsing.enabled": True
}

BASE_LINK = "https://finance.yahoo.com/"

options.add_experimental_option("prefs", PREFS)

driver = Chrome(chrome_options=options)

#Companies
companies = ['PD',
'ZUO',
'PINS',
'ZM',
'PVTL',
'DOCU',
'CLDR',
'RUN'
]

def find_by_id(id, timeout=20, parent=driver):
    finder = lambda d: d.find_element(By.ID, id)
    return WebDriverWait(parent, timeout).until(finder)

def find_by_tag_name(tag_name, timeout=20, parent=driver):
    finder = lambda d: d.find_elements(By.TAG_NAME, tag_name)
    return WebDriverWait(parent, timeout).until(finder)

def find_by_class_name(class_name, timeout=20, parent=driver):
    finder = lambda d: d.find_elements_by_class_name(class_name)
    return WebDriverWait(parent, timeout).until(finder)

def find_by_text(web_list, text):
    i = 0
    try:
        while web_list[i].text != text:
            i+=1
        return web_list[i]
    except:
        return 1

for c in companies:
    driver.get(BASE_LINK)

    search_box = find_by_id("yfin-usr-qry")
    search_box.send_keys(c)
    search_button = find_by_id("header-desktop-search-button")
    search_button.click()

    #If we didn't get company, skipping it
    if "search.yahoo.com" in driver.current_url:
        print(f"Can't find info about {c}")
        continue


    tab_list = find_by_id("quote-nav", timeout=20)
    tabs = find_by_tag_name('li', parent = tab_list)

    try:
        tab_summary = find_by_text(tabs, "Summary")
        if tab_summary==1:
            raise TypeError
    except TypeError:
        print(f"Searching data about {c} failed")
        continue

    tab_summary.click()

    news_data = []
    news_block = find_by_id("quoteNewsStream-0-Stream")
    news_links = find_by_tag_name("a", parent=news_block)
    for n in news_links:
        try:
            news_data.append({
                "title": n.text,
                "link": n.get_attribute('href')
            })
        except:
            pass

    save_news(news_data, c+"_news.csv")

    tab_list = find_by_id("quote-nav", timeout=20)
    tabs = find_by_tag_name('li', parent = tab_list)

    time.sleep(1)
    try:
        tab = find_by_text(tabs,"Historical Data")
        if tab==1:
            raise TypeError
    except TypeError:
        print(f"Searching data about {c} failed")
        continue

    tab.click()

    date_rectangle = find_by_class_name("dateRangeBtn")[0]
    date_rectangle.click()

    buttons = find_by_tag_name('button', parent = date_rectangle)

    try:
        button_Max = find_by_text(buttons, "Max")
        if button_Max==1:
            raise TypeError
    except TypeError:
        print(f"Searching data about {c} failed")
        continue

    button_Max.click()

    block = find_by_id("Col1-1-HistoricalDataTable-Proxy")

    links = find_by_tag_name("a", parent = block)
    FILELIST = listdir()
    try:
        download_link = find_by_text(links,"Download")
        if download_link==1:
            raise TypeError
    except TypeError:
        print(f"Searching data about {c} failed")
        continue

    download_link.click()

    time_start = time.time()
    delta = 0
    TIMEOUT = False
    print(f'Loading data about {c}...')
    #waiting 3 seconds to let chrome download the data
    time.sleep(3)


    try:
        filename = list(set(listdir()) - set(FILELIST))[0]
        update_and_save(filename,c+"_data.csv")
    except:
        print(f"Loading data about {c} failed")

driver.quit()
