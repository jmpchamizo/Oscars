import requests
import json
import os
import pandas as pd
import numpy as np
from exceptions import FilmNotFoundError
from dotenv import load_dotenv

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


def convert_to_genres(id):
    return genres[id]


def get_genresId_dict():
    with open('genres.json') as json_file:
        return json.load(json_file)


genres = get_genresId_dict()

def get_genre(id):
    return [genres[str(e)] if e!=[] and type(e) != str else "" for e in id]


def update_genresId_dict():
    load_dotenv()
    api_key = os.getenv("API_KEY")
    url = f"https://api.themoviedb.org/3/genre/movie/list?api_key={api_key}"
    res = requests.get(url)
    data = {k:v for d in [{e["id"]: e["name"]} for e in res.json()["genres"]] for k,v in d.items()}
    with open('genres.json', 'w') as outfile:
        json.dump(data, outfile)