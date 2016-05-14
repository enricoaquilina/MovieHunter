from general import *
from nltk.tokenize import word_tokenize
import enchant
usa_dict = enchant.Dict('en_US')
gb_dict = enchant.Dict('en_GB')
import string

# white_list = ['hdrip', 'brrip', 'dvdrip', '1080p', 'hc']
black_list = ['hd-tc', 'tc', '480p', 'cam', 'ts', 'scr', 'camrip', 'scrrip', 'hdtc']
language_black_list = ['french', 'russian', 'rus', 'hindi', 'german', 'ita', 'italian', 'punjabi', 'desiscr', 'desi', 'chinese', 'dublado']

def has_seeders(cols):
    seeds = int(cols[2].renderContents())
    if seeds > 0:
        return True

def break_movie_title(raw_title):
    title_parts = word_tokenize(raw_title)

    for part in title_parts:
        if part.__len__() > 20:
            title_parts = raw_title.split('.')

    if len(title_parts) <= 6:
        title_parts = raw_title.split('.')

    if len(title_parts) == 1:
        title_parts = title_parts[0].split(' ')

    return title_parts

def is_high_quality(title_parts):
    for i in range(len(title_parts)):
        for j in range(len(black_list)):
            if black_list[j].lower() in title_parts[i].lower():
                return False
    return True

def is_title_foreign_free(title_parts):
    for i in range(len(title_parts)):
        for j in range(len(language_black_list)):
            if title_parts[i].lower() == language_black_list[j]:
                return False
    return True

def is_title_in_english(film_title):
    film_word_length = len(film_title)
    unrecognized_words = 0

    for i in range(len(film_title)):
        if not usa_dict.check(film_title[i]) and not gb_dict.check((film_title[i])):
            unrecognized_words += 1
    if (unrecognized_words > 0 and unrecognized_words/film_word_length <= 0.5) or len(film_title) == 1 or unrecognized_words == 0:
        return True
    else:
        return False

def get_date_delimeter(title_parts):
    current_year = getDate().year
    date_delimeter = -1

    for i in range(len(title_parts)):
        if contains_string(title_parts[i], str(current_year)):
            date_delimeter = i
            break
        elif contains_string(title_parts[i], str(current_year-1)):
            date_delimeter = i
            break

    return date_delimeter

def parse_film_title(raw_film_title):
    film_title = ''
    for piece in raw_film_title:
        exclude = set(string.punctuation)
        film_title += ''.join(ch for ch in piece if ch not in exclude)+' '

    return film_title.lower().replace('  ', ' ').strip()

def download_movie(magnet_link):
    os.system('transmission-gtk ' + magnet_link)