import random, argparse
from subprocess import check_output
import pandas as pd
import console_utils as con
import numpy as np
import oscars_utils as u
import api_utils as api
import pdf_utils as pu
import matplotlib.pyplot as plt

def main(nfilms, winner, year, genre, filmaffinity, tmdb):
    genres_dict = api.get_genresId_dict()

    result = u.load_oscars_final(filmaffinity, tmdb, year)
    if genre in genres_dict.values():
        list_index = [genre in e for e in result.Genres]
        temp_df = pd.DataFrame(columns = result.columns)
        for i,e in enumerate(list_index):
            if e:
                temp_df = temp_df.append(result.iloc[i], ignore_index = True)
        result = temp_df
    if winner.lower() == "y":
        result = result[result.win == True]
    elif winner.lower() == "n":
        result = result[result.win == False]
    if type(year) == int and year > 1920:
        result = result[result.year_film == year]
    if type(nfilms) == int:
        result = result.iloc[:nfilms].reset_index()
    else:
        result = result.iloc[:5].reset_index()
    pu.create_pdf(result)
    con.print_result(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Devuelve peliculas nominadas o ganadoras de los oscar')
    parser.add_argument('-n', dest='nfilms', default=5, help='Devuelve n peliculas ganadoras o nominadas a los oscars', type=int)
    parser.add_argument('-w', dest='winner', default="", help='(y/n) devuelve peliculas ganadoras de oscars defecto todos', type=str)
    parser.add_argument('-y', dest='year', default=0, help='Devuelve las peliculas de los oscars de ese año', type=int)
    parser.add_argument('-g', dest='genre', default="", help="Devuelve peliculas nominadas por genero ('Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Music','Mystery','Romance','Science Fiction','TV Movie','Thriller','War','Western')", type=str)
    parser.add_argument('-fa', dest='filmaffinity', default="n", help="y actualiza los datos de filmaffinity", type=str)
    parser.add_argument('-tm', dest='tmdb', default="n", help="y actualiza los datos de TheMovieDB", type=str)

    args = parser.parse_args()
    main(args.nfilms, args.winner, args.year, args.genre, args.filmaffinity, args.tmdb)

