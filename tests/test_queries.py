import pandas as pd
import numpy as np
import os
import psycopg2 as pg
import unittest
from dataclasses import dataclass


@dataclass
class Credentials:
    dbname: str = "postgres"
    host: str = "127.0.0.1"
    port: int = 5432
    user: str = "postgres"
    password: str = "1q2w3e"


def psycopg2_conn_string():
    return f"""
            dbname='{os.getenv("DBNAME", Credentials.dbname)}'
            user='{os.getenv("DBUSER", Credentials.user)}'
            host='{os.getenv("DBHOST", Credentials.host)}'
            port='{os.getenv("DBPORT", Credentials.port)}'
            password='{os.getenv("DBPASSWORD", Credentials.password)}'
            """


def set_conntection():
    return pg.connect(psycopg2_conn_string())


class TestHardQueries(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestHardQueries, self).__init__(*args, **kwargs)
        self.connection = set_conntection()
        self.cursor = self.connection.cursor()

    def convert_value(self, value):
        if pd.notna(value):
            return value
        
        return None

    def test1(self):
        query = """
                SELECT g.name, COUNT(m.movie_id) AS total_quantity
                FROM Movies m 
                JOIN MovieGenreConnecter g_m ON m.movie_id = g_m.movie_id
                JOIN Genres g ON g.genre_id = g_m.genre_id
                GROUP BY g.name
                ORDER BY total_quantity DESC
                LIMIT 3;
                """
        result = pd.read_sql(query, con=self.connection)
        assert result.shape == (3, 2)
        expected = [('драма', 11), ('приключения', 7), ('фэнтези', 7)]

        for (id, pair) in enumerate(expected):
            assert result.iloc[id]['name'] == pair[0] and result.iloc[id]['total_quantity'] == pair[1]

    def test2(self):
        query = """
                SELECT p.name, COUNT(r.movie_id) AS total_reviews 
                FROM People p
                JOIN Reviews r ON r.user_id = p.person_id
                GROUP BY p.person_id
                ORDER BY total_reviews DESC;
                """
        result = pd.read_sql(query, con=self.connection)
        assert result.shape == (14, 2)
        expected = [
            ('Alina_23', 2),
            ('Эвелина Штейн', 1),
            ('Stee', 1),
            ('Genious_Fox', 1),
            ('arito_sei', 1),
            ('mickle82', 1),
            ('doctor2', 1),
            ('Евгений Пекло', 1),
            ('Zoso', 1),
            ('Лида Дёгтева', 1),
            ('dinochka-sunny', 1),
            ('Tanatolog', 1),
            ('Fr3ya', 1),
            ('Дмитрий Кожин', 1)
        ]

        for (id, pair) in enumerate(expected):
            assert result.iloc[id]['name'] == pair[0] and result.iloc[id]['total_reviews'] == pair[1]

    def test3(self):
        query = """
                SELECT m.movie_id as id, m.title as film_name, COUNT(r.user_id) AS total_quantity 
                FROM Movies m
                JOIN ReviewsHistory r ON r.movie_id = m.movie_id
                WHERE r.date_added BETWEEN CURRENT_DATE - INTERVAL '6 month' AND CURRENT_DATE
                GROUP BY m.movie_id
                ORDER BY total_quantity DESC;
                """
        result = pd.read_sql(query, con=self.connection)
        assert result.shape == (1, 3)
        assert result.iloc[0]['id'] == 1
        assert result.iloc[0]['film_name'] == 'Зеленая миля'
        assert result.iloc[0]['total_quantity'] == 2

    def test4(self):
        query = """
                SELECT p.name, ROUND(AVG(r.rating)) as avg_rating
                FROM People p
                JOIN MovieActorConnecter m_a ON p.person_id = m_a.actor_id
                JOIN Reviews r ON r.movie_id = m_a.movie_id
                GROUP BY p.person_id;
                """
        result = pd.read_sql(query, con=self.connection)
        assert result.shape == (28, 2)
        expected = [
            ("Робин Райт", 8),
            ("Джон Рис-Дэвис", 8),
            ("Дэвид Морс", 9),
            ("Орландо Блум", 8),
            ("Иэн Маккеллен", 8),
            ("Тим Роббинс", 4),
            ("Эдди Мёрфи", 2),
            ("Хелена Бонэм Картер", 3),
            ("Юрий Яковлев", 10),
            ("Лиам Нисон", 9),
            ("Бен Кингсли", 9),
            ("Брэд Питт", 3),
            ("Мэттью Макконахи", 9),
            ("Джон Траволта", 5),
            ("Майк Майерс", 2),
            ("Омар Си", 4),
            ("Брюс Уиллис", 5),
            ("Вигго Мортенсен", 8),
            ("Франсуа Клюзе", 4),
            ("Лив Тайлер", 8),
            ("Леонид Куравлёв", 10),
            ("Ума Турман", 5),
            ("Сэмюэл Л. Джексон", 5),
            ("Элайджа Вуд", 8),
            ("Эдвард Нортон", 3),
            ("Энн Хэтэуэй", 9),
            ("Морган Фримен", 4),
            ("Том Хэнкс", 8),
        ]

        for (id, pair) in enumerate(expected):
            assert result.iloc[id]['name'] == pair[0] and result.iloc[id]['avg_rating'] == pair[1]

    def test5(self):
        query = """
                WITH diff AS (
                SELECT m.title as film_name, g.name as genre,
                m.release_date AS current_date, LAG(m.release_date) OVER (
                PARTITION BY g.name
                ORDER BY m.release_date) as prev_date
                FROM Movies m
                JOIN MovieGenreConnecter g_m ON m.movie_id = g_m.movie_id
                JOIN Genres g ON g.genre_id = g_m.genre_id)
                SELECT film_name, genre,
                CASE WHEN prev_date is NULL THEN NULL
                ELSE current_date - prev_date
                END difference
                FROM diff;
                """
        result = pd.read_sql(query, con=self.connection)
        drama = []
        assert result.shape == (53, 3)
        expected = [
            ("Побег из Шоушенка", None), 
            ("Зеленая миля", 9012),
            ("Криминальное чтиво", 8481),
            ("Властелин колец - Братство Кольца", 8129),
            ("Властелин колец - Две крепости", 7823),
            ("Властелин колец - Возвращение короля", 7555),
            ("Список Шиндлера", 7284),
            ("Бойцовский клуб", 7158),
            ("Форрест Гамп", 6113),
            ("1+1", 5268),
            ("Интерстеллар", 4359)
        ]

        for id in range(len(result)):
            if result.iloc[id]['genre'] == 'драма':
                drama.append((result.iloc[id]['film_name'], result.iloc[id]['difference']))

        for (id, pair) in enumerate(expected):
            assert drama[id][0] == pair[0] and self.convert_value(drama[id][1]) == pair[1]

    def test6(self):
        query = """
                SELECT m.title, COUNT(a.award_id) as awards_amount, RANK() OVER (
                ORDER BY COUNT(a.award_id) DESC)
                FROM Movies m
                JOIN AwardMovieConnecter a_m ON m.movie_id = a_m.movie_id
                JOIN Awards a ON a.award_id = a_m.award_id
                GROUP BY m.movie_id;
                """
        result = pd.read_sql(query, con=self.connection)
        assert result.shape == (10, 3)
        expected = [
            ("Интерстеллар", 4, 1),
            ("Форрест Гамп", 2, 2),
            ("1+1", 2, 2),
            ("Зеленая миля", 1, 4),
            ("Властелин колец - Братство Кольца", 1, 4),
            ("Унесённые призраками", 1, 4),
            ("Побег из Шоушенка", 1, 4),
            ("Властелин колец - Возвращение короля", 1, 4),
            ("Властелин колец - Две крепости", 1, 4),
            ("Криминальное чтиво", 1, 4),
        ]

        for (id, pair) in enumerate(expected):
            assert result.iloc[id]['title'] == pair[0] \
                and result.iloc[id]['awards_amount'] == pair[1] \
                and result.iloc[id]['rank'] == pair[2]

    def test7(self):
        query = """
                SELECT DISTINCT p.name
                FROM People p 
                JOIN ComposerSoundtrackConnecter c_s ON p.person_id = c_s.composer_id
                JOIN Soundtracks s ON s.soundtrack_id = c_s.soundtrack_id
                JOIN AwardMovieConnecter a_m ON s.movie_id = a_m.movie_id
                GROUP BY p.name, s.soundtrack_id, s.movie_id
                HAVING COUNT(a_m.award_id) > 2;
                """
        result = pd.read_sql(query, con=self.connection)
        assert result.shape == (1, 1)
        assert result.iloc[0]['name'] == 'Ханс Циммер'

    def test8(self):
        query = """
                SELECT o.title, o.release_date AS original_date, r.release_date AS remake_date
                FROM Movies o JOIN Movies r ON r.movie_id = o.remake_id;
                """
        result = pd.read_sql(query, con=self.connection)
        assert result.shape == (3, 3)

        for i in range(3):
            assert result.iloc[i]['title'] == 'Звезда Родилась'

    def test9(self):
        query = """
                SELECT DISTINCT p.name
                FROM People p
                JOIN ComposerSoundtrackConnecter c_s ON p.person_id = c_s.composer_id
                JOIN Soundtracks s ON s.soundtrack_id = c_s.soundtrack_id
                JOIN AwardMovieConnecter a_m ON s.movie_id = a_m.movie_id
                JOIN AwardPersonConnecter a_p ON p.person_id = a_p.person_id;
                """
        result = pd.read_sql(query, con=self.connection)
        assert result.shape == (2, 1)
        names = ['Говард Шор', 'Томас Ньюман']

        for (i, name) in enumerate(names):
            assert result.iloc[i]['name'] == name

    def test10(self):
        query = """
                SELECT m.movie_id as id, m.title as film_name,
                AVG(w_r.rating) as woman_rating, AVG(m_r.rating) as man_rating
                FROM Movies m LEFT JOIN (
                SELECT r.rating as rating, r.movie_id as id
                FROM Reviews r
                JOIN People p ON r.user_id = p.person_id
                WHERE p.gender = 'female') w_r
                ON m.movie_id = w_r.id
                LEFT JOIN (SELECT r.rating as rating, r.movie_id as id
                FROM Reviews r
                JOIN People p ON r.user_id = p.person_id
                WHERE p.gender = 'male') m_r ON m.movie_id = m_r.id
                GROUP BY m.movie_id;
                """
        result = pd.read_sql(query, con=self.connection)
        assert result.shape == (19, 4)
        expected = [
            (8, "Властелин колец - Возвращение короля", 7.9, None),
            (11, "Шрэк", 2, None),
            (19, "Звезда Родилась", None, None),
            (4, "Побег из Шоушенка", 4, None),
            (14, "Ходячий замок", None, 4.2),
            (3, "Форрест Гамп", 8, None),
            (17, "Звезда Родилась", None, None),
            (7, "Бойцовский клуб", 3.3, None),
            (13, "Властелин колец - Две крепости", 9, None),
            (10, "Список Шиндлера", None, 8.9),
            (9, "Криминальное чтиво", None, 5),
            (1, "Зеленая миля", 9, None),
            (5, "Интерстеллар", None, 8.6),
            (18, "Звезда Родилась", None, None),
            (2, "1+1", None, 3.5),
            (16, "Звезда Родилась", None, None),
            (15, "Властелин колец - Братство Кольца", 8, None),
            (6, "Унесённые призраками", None, 9.5),
            (12, "Иван Васильевич меняет профессию", None, 10),
        ]

        for (id, pair) in enumerate(expected):
            assert result.iloc[id]['id'] == pair[0] \
                and result.iloc[id]['film_name'] == pair[1] \
                and self.convert_value(result.iloc[id]['woman_rating']) == pair[2] \
                and self.convert_value(result.iloc[id]['man_rating']) == pair[3]

    def end(self):
        self.cursor.close()
        self.connection.close()


if __name__ == '__main__':
    unittest.main()
