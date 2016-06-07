import requests
from movie import *
from bs4 import BeautifulSoup
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = 'Movie_Hunter'
create_project_directory(PROJECT_NAME)

count = -1
print('Initialising the Hunt!')

while count < 4:

    if count == -1:
        r = requests.get("http://thepiratebay.se/browse/201")
        count += 1
    elif count > -1:
        r = requests.get("http://thepiratebay.se/browse/201/"+str(count)+"/3")
        count += 1

    print('\nHunting Page '+str(count)+"!")
    soup = BeautifulSoup(r.content, "lxml")
    table = soup.find('table', {'id': 'searchResult'})

    try:
        for row in table.findAll("tr"):
            cols = row.findAll('td')
            if cols.__len__() > 1:
                if has_seeders(cols):
                    links = get_all_links(cols[1])
                    dateUploaded = get_upload_text(cols[1])
                    allowed_upload_times = ['Today', 'ago', 'Y-day']
                    if contains_set_string(break_movie_title(dateUploaded), allowed_upload_times):
                        title_parts = break_movie_title(links[0].text)
                        date_delimeter = get_date_delimeter(title_parts)

                        if date_delimeter > -1:
                            film_year = clean(title_parts[date_delimeter])
                            film_title = parse_film_title(title_parts[0:date_delimeter])
                            if only_roman_chars(film_title):
                                if is_title_foreign_free(title_parts):
                                    if is_title_in_english(break_movie_title(film_title)):
                                        if is_high_quality(title_parts):
                                            if check_imdb_lang(film_title, film_year):
                                                if does_file_exist(PROJECT_PATH, PROJECT_NAME, film_year):
                                                    if does_film_exist(PROJECT_PATH, PROJECT_NAME, film_title, film_year):
                                                        download_movie(links[1]['href'])
                                                        print('Downloading '+film_title)
                                                        append_to_file(PROJECT_PATH+'/'+PROJECT_NAME + '/Year_'+film_year+'.txt', film_title)

    except Exception as ex:
        print('An error occurred!')
        print(ex)

order_films(PROJECT_PATH, PROJECT_NAME)

