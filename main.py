import requests
from movie import *
from bs4 import BeautifulSoup
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECT_NAME = 'Movie_Hunter'
create_project_directory(PROJECT_NAME)

count = -1
print('Initialising the Hunt!')

def do_download_process(magnet_link, movie_title, movie_year):

            res = download_movie(magnet_link)
            print('Downloading ' + movie_title)
            append_to_file(PROJECT_PATH + '/' + PROJECT_NAME + '/Year_' + movie_year + '.txt', movie_title)

while count < 4:

    if count == -1:
        r = requests.get("http://thepiratebay.se/browse/201")
        count += 1
    elif count > -1:
        r = requests.get("http://thepiratebay.se/browse/201/"+str(count)+"/3")
        count +=1

    print('\nHunting Page '+str(count)+"!")
    soup = BeautifulSoup(r.content, "lxml")
    table = soup.find('table', {'id': 'searchResult'})

    try:
        if table != None:
            for row in table.findAll("tr"):
                cols = row.findAll('td')
                if cols.__len__() > 1:
                    seeders = get_seeders(cols)
                    if seeders > 0:
                        links = get_all_links(cols[1])
                        dateUploaded = get_upload_text(cols[1])
                        allowed_upload_times = ['Today', 'ago', 'Y-day']
                        if contains_set_string(break_movie_title(dateUploaded), allowed_upload_times):
                            title_parts = break_movie_title(links[0].text)
                            date_delimeter = get_date_delimeter(title_parts)

                            if date_delimeter > -1:
                                successful, film_year = clean(title_parts[date_delimeter])
                                if successful:
                                    if date_delimeter > 0:
                                        film_title = parse_film_title(title_parts[0:date_delimeter])
                                    else:
                                        # remove numbers from string
                                        film_title = parse_film_title(title_parts[0])
                                    if only_roman_chars(film_title):
                                        if is_title_foreign_free(title_parts):
                                            # if is_title_in_english(break_movie_title(film_title)):
                                                if is_high_quality(title_parts):
                                                    if does_file_exist(PROJECT_PATH, PROJECT_NAME, film_year):
                                                        if does_film_exist(PROJECT_PATH, PROJECT_NAME, film_title, film_year):
                                                            is_eng = check_imdb_lang(film_title, film_year)
                                                            if is_eng:
                                                                do_download_process(links[1]["href"], film_title, film_year)
        else:
            print('TPB is down!!')


    except Exception as ex:
        print('An error occurred!')
        print(ex)

order_films(PROJECT_PATH, PROJECT_NAME)

