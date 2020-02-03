import pandas as pd
import json
import api_utils as api
import scrapping_utils as sc


def load_oscars_final(filmaffinity="", tmdb="", year="0"):
    #Cargamos el dataframe que hemos escogido:
    oscars = pd.read_csv("../INPUT/the_oscar_award.csv")
    TheMovieDB_df = pd.DataFrame()
    film_df = pd.DataFrame()

    #Como se tarda mucho en actualizar los datos de filmaffinity y TMDB hacemos
    #la prueba solo con un año, si se mete por consola usaremos ese, sino el 2018
    year = 2018 if year == 0 else year
    print(year)
    if filmaffinity.lower == "y" or tmdb=="y":
        oscars == oscars[oscars.year_film == year]

    #Si el usuario quiere que actualicemos los datos de tmdb
    if tmdb.lower() == "y":
        TheMovieDB_df = load_tmdb_api(oscars.film, oscars.year_film, oscars)
    else:
    #sino cargamos los datos ya guardados en json de una petición anterior:
        with open('TheMovieDB_json.json') as json_file:
            TheMovieDB_json = json.load(json_file)
        data = {'Original_Title': TheMovieDB_json[0]["original_title"], 'Release_Date': TheMovieDB_json[1]["release_date"],'Genre_Ids': TheMovieDB_json[2]["genre_ids"], 'Poster_Path': TheMovieDB_json[3]["poster_path"] }
        TheMovieDB_df = pd.DataFrame(data = data)


    #Cambiamos los genreids a genre:
    TheMovieDB_df["Genres"] = TheMovieDB_df.Genre_Ids.apply(api.get_genre)
    TheMovieDB_df["Genres"] = TheMovieDB_df.Genres.apply(lambda x: ",".join(x))


    #Si el usuario quiere que actualicemos los datos de filmaffinity
    if filmaffinity.lower() == "y":
        load_filmaffinity_web(oscars.film, oscars.year_film)
    else:
    #sino argamos los datos de Filmaffinity desde JSON:
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

def load_filmaffinity_web(titles, years):
    #Scrappear los datos de filmaffinity
    return sc.get_properties_film_filmaffinity(titles, years)


def load_tmdb_api(titles, years, dataframe):
    #Cogemos los datos de TheMovieDB con su API:
    return api.get_properties_film(titles, years, dataframe, properties=["original_title", "release_date", "genre_ids", "poster_path"])