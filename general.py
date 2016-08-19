import os
import datetime
import unicodedata as ud
import os

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
latin_letters = {}

def get_all_links(important_column):
    return important_column.findAll('a', href=True)

def get_upload_text(important_column):
    return important_column.findAll('font', {'class': 'detDesc'})[0].text

def getDate():
    return datetime.datetime.now()

def create_project_directory(directory):
    if not os.path.exists(PROJECT_PATH + '/' + directory):
        print('Creating project ' + directory)
        os.makedirs(PROJECT_PATH + '/' + directory)

def write_file(file_name, contents):
    f = open(file_name, 'w')
    f.write(contents)
    f.close()

def append_to_file(file_name, contents):
    with open(file_name, 'a') as file:
        file.write(contents + '\n')

def delete_file_contents(file_name):
    with open(file_name, 'w'):
        pass

def file_to_set(file_name):
    results = set()
    with open(file_name, 'rt') as f:
        for line in f:
            results.add(line.replace('\n', ''))
    return results

def set_to_file(linkSet, file):
    delete_file_contents(file)
    for line in sorted(linkSet):
        append_to_file(file, line)
    return file

def order_films(path, PROJECT_NAME):
    current_date = getDate().year


    current_year_file = os.path.dirname(os.path.realpath(__file__))  + '/' + PROJECT_NAME + '/Year_' + str(current_date) + '.txt'
    previous_year_file = os.path.dirname(os.path.realpath(__file__)) + '/' + PROJECT_NAME + '/Year_' + str((current_date-1)) + '.txt'

    previous_year_set = file_to_set(previous_year_file)
    current_year_set = file_to_set(current_year_file)

    set_to_file(previous_year_set, previous_year_file)
    set_to_file(current_year_set, current_year_file)

def contains_string(root, filter):
    try:
        test = root.index(filter)
    except Exception:
        return False

    return True

def contains_set_string(root, filters):
    for i in range(len(root)):
        for j in range(len(filters)):
            if root[i].lower() == filters[j].lower():
                return True
    return False

def does_file_exist(project_path, project_name, year):
    file_name = project_path + '/' + project_name + '/Year_' + year + '.txt'
    if not os.path.isfile(file_name):
       write_file(file_name, '')
    return True

def does_film_exist(project_path, project_name, film_title, year):
    available_films = file_to_set(project_path + '/' + project_name + '/Year_' + year + '.txt')

    for existing_film in available_films:
        if film_title not in existing_film:
            continue
        else:
            return False
    return True

def clean(dirty_text):
    dirty_text = dirty_text.replace('(', '')
    clean_text = dirty_text.replace(')', '')
    # print(clean_text)
    if is_number(clean_text):
        return True, clean_text
    return False, ''

def is_latin(uchr):
    try: return latin_letters[uchr]
    except KeyError:
         return latin_letters.setdefault(uchr, 'LATIN' in ud.name(uchr))

def only_roman_chars(unistr):
    return all(is_latin(uchr)
           for uchr in unistr
           if uchr.isalpha())


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False