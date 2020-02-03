# Oscars

<p>Partimos de un dataframe todas las nominaciones de los Oscars: https://www.kaggle.com/unanimad/the-oscar-award. Hay que tener en cuenta que hay nominaciones que no se hacen a una pelicula en concreto y estos campos aparecen vacios.</p>

<p>Lo enriquecemos a traves de la API de TheMovieDB cogiendo los campos Genres y la url del poster de la película. Además, haciendo web scrapping a Filmaffinity cogemos la valoración y descriptición de la pelicua.</p>

<p>Creamos una función para que nos devuelva estas nominaciones según una serie de filtros</p>

## Parámetros de la función main

<p>En la función main tiene siete parámetros:</p>
<p>Los dos primeros que vamos a explicar tiene información de cómo se cargan los datos. En el proyecto hay un json de datos precargados de la API de TheMovieDB y de filmaffinity, así que si dejamos no indicamos nada en esos camops se cogeran los datos de los json precargados.</p>
<ul>
<li>-fa: "y" Hará que se conecte con Filmaffinity y los datos los datos.</li>
<li>-tm: "y" Hará que se conecte con TheMovieDB y actualice los datos.</li>
</ul>
<p>Asi la función loads_oscar_final se encarga de coger esos datos y crear un único dataframe con las columnas del csv más las dos que hemos indicado de Filmaffinity y TheMovieDB</p>
<ul>
<li>-g Filtra por genero siendo los valores permitidos: Action','Adventure','Animation','Comedy','Crime','Documentary','Drama','Family','Fantasy','History','Horror','Music','Mystery','Romance','Science Fiction','TV Movie','Thriller','War','Western'.</li>
<li>-y Fitra por año desde el 1921-2019.</li>
<li>-w Filtra por ganadores: y o nominados: n.</li>
<li>-n Mostrará los n primeros valores que coincidan con los campos de busqueda.</li>
<li>-wl La salida de esta opción depende de -w si ponemos a True -wl y w esta a y sacará la media de la valoración de las peliculas ganadoras con los filtros anteriores, si w esta a "n" sacará la media de la valoración de las peliculas nominadas con el resto de filtros, pero si n no tiene valor hará un gráfico de la media de la valoración de peliculas ganadoras y nominadas aplicados los filtros anteriores.</li>
</ul>

<p>La inforamción de las peliculas aplicados los filtros también se muestra en un pdf que se guarda en fichero del proyecto.</p>
    