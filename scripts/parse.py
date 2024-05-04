import re

MONTH_TABLE = {
    "января": 1,
    "февраля": 2,
    "марта": 3,
    "апреля": 4,
    "мая": 5,
    "июня": 6,
    "июля": 7,
    "августа": 8,
    "сентября": 9,
    "октября": 10,
    "ноября": 11,
    "декабря": 12,
}

def wrap_string(string):
    return "\'" + string.strip() + "\'"

def find_idx_by_pattern(text, pattern):
    for i in range(len(text)):
        if len(re.findall(pattern, text[i])) != 0:
            return i

    assert(False)

def parse_title(text):
    name_pattern = re.compile(r"Название:")
    value_pattern = re.compile(r"[^(]*")
    title = parse_common(text, name_pattern, value_pattern)
    return wrap_string(title.replace(":", ""))

def parse_duration(text):
    name_pattern = re.compile(r"Время:")
    value_pattern = re.compile(r"\d+:\d+")
    duration = parse_common(text, name_pattern, value_pattern)
    return wrap_string(duration)

def parse_release_date(text):
    name_pattern = re.compile(r"Релиз на DVD:")
    value_pattern = re.compile(r"[^,]*")
    release_date = parse_common(text, name_pattern, value_pattern)
    release_date = release_date.split()
    release_date[1] = str(MONTH_TABLE[release_date[1]])
    (day, month, year) = map(int, release_date)
    release_date = "{:04d}-{:02d}-{:02d}".format(year, month, day)
    return wrap_string(release_date)

def parse_genre(text):
    name_pattern = re.compile(r"Жанр:")
    value_pattern = re.compile(r".*")
    genre = parse_common(text, name_pattern, value_pattern)
    return wrap_string(genre)

def parse_composer(text):
    name_pattern = re.compile(r"Композитор:")
    value_pattern = re.compile(r".*")
    genre = parse_common(text, name_pattern, value_pattern)
    return wrap_string(genre)

def parse_director(text):
    name_pattern = re.compile(r"Режиссер:")
    value_pattern = re.compile(r".*")
    genre = parse_common(text, name_pattern, value_pattern)
    return wrap_string(genre)

def parse_common(text, name_pattern, value_pattern):
    idx = find_idx_by_pattern(text, name_pattern)
    start = text[idx].find(":") + 1
    value = re.findall(value_pattern, text[idx][start:])
    return value[0]
