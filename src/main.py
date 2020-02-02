from subprocess import check_output
import pandas as pd
import random
import argparse
import numpy as np
import utils as u




def bash_command(cmd):
    return check_output(['/bin/bash', '-c', cmd]).decode('utf-8')

def main(nfilms, winner, year, genre):
    genres_dict = u.get_genresId_dict()
    result = u.load_oscars_final()
    if genre in genres_dict.values():
        t = [genre in e for e in result.Genres]
        d = np.array([t,]*9).transpose()
        result = result * d
        result = result [result.Genres]
    if winner.lower() == "y":
        result = result[result.win == True]
    if winner.lower() == "n":
        result = result[result.win == False]
    if type(year) == int and year > 1920:
        result = result[result.year_film == year]
    if type(nfilms) == int:
        print(result.iloc[:nfilms])
    else:
        print(result.iloc[:5])

#
#    voices = voices.split("\n")
#    voices = list(map(lambda x: x.split(" ")[0],voices))[0:-1]
#    voices = bash_command('say --voice="?"')
#    selectedVoice = random.choice(voices)
#
#    ta = random.choice(["Felipe","Fran","Ovi","Blanca","Clara"])
#    frase = f"Hola {ta}"
#    print(f"Saludando a {ta} con la voz de {selectedVoice}")
#
#    print(f"Saludando {nVeces}...")
#    for n in range(nVeces):
#        bash_command(f'say --voice "{selectedVoice}" "{frase}"')
#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Devuelve peliculas nominadas o ganadoras de los oscar')
    parser.add_argument('-n', dest='nfilms', default=5, help='Devuelve n peliculas ganadoras o nominadas a los oscars', type=int)
    parser.add_argument('-w', dest='winner', default="", help='(y/n) devuelve peliculas ganadoras de oscars defecto todos', type=str)
    parser.add_argument('-y', dest='year', default=0, help='Devuelve las peliculas de los oscars de ese año', type=int)
    parser.add_argument('-g', dest='genre', default="", help="Devuelve peliculas nominadas por genero ('Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Music','Mystery','Romance','Science Fiction','TV Movie','Thriller','War','Western')", type=str)
    args = parser.parse_args()
    main(args.nfilms, args.winner, args.year, args.genre)


