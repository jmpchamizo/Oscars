import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

def find_filmaffinity_film(film, year, driver = None):
    if driver == None:
        diver = webdriver.Chrome()
    driver.get("https://www.filmaffinity.com/es/main.html")
    element = driver.find_element_by_xpath("//input[@id='top-search-input']")
    element.send_keys(film, Keys.ENTER)
    if "https://www.filmaffinity.com/es/search.php?" in driver.current_url:
        search_film_filmaffinity(driver, year)
    return get_filmaffinity_rate_description(driver)

def search_film_filmaffinity(driver, year):
    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')
    for film in soup.select('div[class^="se-it"]'):
        for div in film.findChildren():
            if "class" in div.attrs.keys() and "ye-w" in div.attrs["class"] and re.search("(\d){4}",div.text.strip()):
                year_film = int(div.text.strip())
                for y in range(int(year)-1,int(year)+2):
                    if  year_film == y:
                        for div in film.findChildren():
                            if "class" in div.attrs.keys() and "mc-title" in div.attrs["class"]:
                                return driver.get([tag.attrs["href"] for tag in div.findChildren() if "href" in tag.attrs][0])

def get_filmaffinity_rate_description(driver):
    data = driver.page_source
    soup = BeautifulSoup(data, 'html.parser')
    r = soup.select_one('div[id^="movie-rat-avg"]')
    d = soup.select_one('dd[itemprop^="description"]')
    if r != None:
        rate = float(soup.select_one('div[id^="movie-rat-avg"]').text.strip().replace(",", "."))
    else:
        rate = ""
    if d != None:
        description = soup.select_one('dd[itemprop^="description"]').text.strip()
    else:
        description = ""
    return [rate, description]



def get_properties_film_filmaffinity(titles, years):
    driver = webdriver.Chrome()
    result = []
    for i in titles.index:
        try:
            result.append(find_filmaffinity_film(titles[i], years[i], driver))
        except:
            return pd.DataFrame(np.array(result), columns=["Rate", "Description"])
    driver.quit()
    return pd.DataFrame(np.array(result), columns=["Rate", "Description"])
