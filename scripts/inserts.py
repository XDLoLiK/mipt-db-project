import os
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from parse import *
from id_table import *

NAME_TABLE = {
    "Название": "title",
    "Время": "duration",
    "Релиз на DVD": "release_date",
    "Жанр": "genre",
    "Композитор": "composer",
    "Режиссер": "director",
}

HANDLER_TABLE = {
    "Название": parse_title,
    "Время": parse_duration,
    "Релиз на DVD": parse_release_date,
    "Жанр": parse_genre,
    "Композитор": parse_composer,
    "Режиссер": parse_director,
}

def load_page(driver, url, timeout=5):
    driver.get(url)
    WebDriverWait(driver, timeout).until(
        lambda drv: drv.find_element(By.CLASS_NAME, "body")
    )
    return driver.page_source

def get_movie_links(driver, count):
    url = "https://www.kinopoisk.ru/lists/movies/top250"
    source = load_page(driver, url, 60)
    soup = BeautifulSoup(source, "html.parser")
    class_regex = re.compile(r"base-movie-main-info_link.*")
    return soup.find_all("a", { "class": class_regex })[:count]

def get_movie_data(soup):
    data = {}
    title = soup \
        .find("h1", { "class": re.compile(r"styles_title.*") }) \
        .find("span") \
        .text
    data["title"] = parse_title(title)
    ID_TABLE.add_object("title", data["title"])

    for div in soup.find_all("div", { "data-tid": re.compile(r"7cda04a5") }):
        inner = div.find_all("div", recursive=False)
        name = inner[0].text

        try:
            content = inner[1].find("a").text
        except AttributeError:
            content = inner[1].find("div").text

def main():
    driver = webdriver.Chrome()
    movies_data = []
    links = get_movie_links(driver, 15)

    for a in links:
        url = "https://www.kinopoisk.ru" + a["href"]
        film_page = load_page(driver, url)
        soup = BeautifulSoup(film_page, "html.parser")
        data = get_movie_data(soup)
        movies_data.append(data)

if __name__ == "__main__":
    load_dotenv()
    FILE_PATH = os.getenv("FILE_PATH")
    main()
