import re
import pandas as pd
import numpy as np
import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from exceptions import FilmNotFoundError
from bs4 import BeautifulSoup
from dotenv import load_dotenv



#API
def request_TheMobieDB(title, year = 0):
    load_dotenv()
    api_key = os.getenv("API_KEY")
    baseUrl = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query="
    url = baseUrl + title.strip().replace(" ", "+")
    res = requests.get(url)
    if res.json()['total_results'] == 0:
        raise FilmNotFoundError
    elif res.json()['total_results'] > 0 and year != 0:
        for e in res.json()["results"]:
            for y in range(int(year)-1,int(year)+2):
                if 'release_date' in e.keys() and e['release_date'].split("-")[0] != "" and int(e['release_date'].split("-")[0]) == y:
                    return e
        raise FilmNotFoundError
    return res.json()["results"][0]


def get_properties_film(titles, years, dataframe, properties=[]):
    result = []
    for i,_ in enumerate(titles):
        if titles[i] == " ":
            result.append([""]*len(properties))
            continue
        try:
            json_temp = request_TheMobieDB(titles[i], years[i])
        except FilmNotFoundError:
            result.append(["Film not found"]*len(properties))
            continue
        temp_list = []
        for property in properties:
            temp_list.append(json_temp[property])              
        result.append(temp_list)
    return pd.DataFrame(np.array(result), columns=properties)



def get_genresId_dict():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}"
    res = requests.get(url)
    return {k:v for d in [{e["id"]: e["name"]} for e in res.json()["genres"]] for k,v in d.items()}

genres = get_genresId_dict()
def convert_to_genres(id):
    genres = get_genresId_dict()
    return genres[id]


def get_genre(id):
    return [genres[e] if e!=[] and type(e) != str else "" for e in id]


#Selenium:
def find_filmaffinity_film(film, year, driver = webdriver.Chrome()):
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


def load_oscars_final():
    #Cargamos el dataframe que hemos escogido:
    oscars = pd.read_csv("../INPUT/the_oscar_award.csv")


    #Cogemos los datos de TheMovieDB con su API:
    #TheMovieDB_df = get_properties_film(oscars.film, oscars.year_film, oscars, properties=["original_title", "release_date", "genre_ids", "poster_path"])

    #Si queremos cargar los datos ya guardados en json de una petició anterior:
    with open('TheMovieDB_json.json') as json_file:
        TheMovieDB_json = json.load(json_file)

    data = {'Original_Title': TheMovieDB_json[0]["original_title"], 'Release_Date': TheMovieDB_json[1]["release_date"],'Genre_Ids': TheMovieDB_json[2]["genre_ids"], 'Poster_Path': TheMovieDB_json[3]["poster_path"] }
    TheMovieDB_df = pd.DataFrame(data = data)


    #Cambiamos los genreids a genre:
    TheMovieDB_df["Genres"] = TheMovieDB_df.Genre_Ids.apply(get_genre)
    TheMovieDB_df["Genres"] = TheMovieDB_df.Genres.apply(lambda x: ",".join(x))

    #Scrappear los datos de filmaffinity
    #film_df = u.get_properties_film_filmaffinity(oscars.film, oscars.year_film)

    #Cargar los datos de Filmaffinity desde JSON:
    with open('filmaff_json.json') as json_file:
        film_json = json.load(json_file)

    data = {'Rate': film_json[0]["Rate"], 'Description': film_json[1]["Description"]}
    film_df = pd.DataFrame(data = data)
 
    #Contruimos el dataframe final:
    oscars["Genres"] = TheMovieDB_df["Genres"]
    oscars["Poster"] = TheMovieDB_df["Poster_Path"]
    oscars["Description"] = film_df["Description"]
    oscars["Rate"] = film_df["Rate"]
    #El df final con el que trabajaremos será:
    return oscars[["film", "year_film", "category", "name", "win", "Genres", "Rate", "Description", "Poster"]]

