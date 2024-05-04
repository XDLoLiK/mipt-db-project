-- Active: 1709919509361@@127.0.0.1@5432@postgres@public

-- Топ 3 категории по популярности
SELECT g.name, COUNT(m.movie_id) AS total_quantity
FROM
    Movies m
    JOIN MovieGenreConnecter m_g ON m.movie_id = m_g.movie_id
    JOIN Genres g ON g.genre_id = m_g.genre_id
GROUP BY
    g.name
ORDER BY total_quantity DESC
LIMIT 3;

-- Самые активные обзорщики
SELECT p.name, COUNT(r.movie_id) AS total_reviews
FROM People p
    JOIN Reviews r ON r.user_id = p.person_id
GROUP BY
    p.person_id
ORDER BY total_reviews DESC;

-- Самые популярные по обзорам фильмы за последние полгода
SELECT
    m.movie_id as id,
    m.title as film_name,
    COUNT(r.user_id) AS total_quantity
FROM Movies m
    JOIN ReviewsHistory r ON r.movie_id = m.movie_id
WHERE
    r.date_added BETWEEN CURRENT_DATE - INTERVAL '6 month' AND CURRENT_DATE
GROUP BY
    m.movie_id
ORDER BY total_quantity DESC;

-- Для каждого актёра посчитаем средний рейтинг фильмов, в которых он снимался
SELECT p.name, ROUND(AVG(r.rating)) as avg_rating
FROM
    People p
    JOIN MovieActorConnecter m_a ON p.person_id = m_a.actor_id
    JOIN Reviews r ON r.movie_id = m_a.movie_id
GROUP BY
    p.person_id;

-- Разница даты выпуска фильма с предыдущим по времени в той же категории
WITH
    diff AS (
        SELECT
            m.title as film_name, g.name as genre, m.release_date AS current_date, LAG(m.release_date) OVER (
                PARTITION BY
                    g.name
                ORDER BY m.release_date
            ) as prev_date
        FROM
            Movies m
            JOIN MovieGenreConnecter g_m ON m.movie_id = g_m.movie_id
            JOIN Genres g ON g.genre_id = g_m.genre_id
    )
SELECT
    film_name,
    genre,
    CASE
        WHEN prev_date is NULL THEN NULL
        ELSE current_date - prev_date
    END difference
FROM diff;

-- Ранжированный список фильмов по количеству их наград
SELECT m.title, COUNT(a.award_id) as awards_amount, RANK() OVER (
        ORDER BY COUNT(a.award_id) DESC
    )
FROM
    Movies m
    JOIN AwardMovieConnecter a_m ON m.movie_id = a_m.movie_id
    JOIN Awards a ON a.award_id = a_m.award_id
GROUP BY
    m.movie_id;

-- Список композиторов, писавших саундтрек к фильмам, получившим хотя бы 2 награды
SELECT DISTINCT
    p.name
FROM
    People p
    JOIN ComposerSoundtrackConnecter c_s ON p.person_id = c_s.composer_id
    JOIN Soundtracks s ON s.soundtrack_id = c_s.soundtrack_id
    JOIN AwardMovieConnecter a_m ON s.movie_id = a_m.movie_id
GROUP BY
    p.name,
    s.soundtrack_id,
    s.movie_id
HAVING
    COUNT(a_m.award_id) > 2;

-- Список фильмов, имеющих ремейки, с датой выхода оригинала и ремейка
SELECT
    r.title,
    r.release_date AS remake_date,
    o.release_date AS original_date
FROM Movies r
    JOIN Movies o ON o.movie_id = r.remake_id;

-- Список композиторов, которые получили награду за фильм, у которого тоже есть какая-то награда
SELECT DISTINCT
    p.name
FROM
    People p
    JOIN ComposerSoundtrackConnecter c_s ON p.person_id = c_s.composer_id
    JOIN Soundtracks s ON s.soundtrack_id = c_s.soundtrack_id
    JOIN AwardMovieConnecter a_m ON s.movie_id = a_m.movie_id
    JOIN AwardPersonConnecter a_p ON p.person_id = a_p.person_id;

-- Для каждого фильма посчитаем его среднюю оценку от женщин и мужчин
SELECT
    m.movie_id as id,
    m.title as film_name,
    AVG(w_r.rating) as woman_rating,
    AVG(m_r.rating) as man_rating
FROM Movies m
    LEFT JOIN (
        SELECT r.rating as rating, r.movie_id as id
        FROM Reviews r
            JOIN People p ON r.user_id = p.person_id
        WHERE
            p.gender = 'female'
    ) w_r ON m.movie_id = w_r.id
    LEFT JOIN (
        SELECT r.rating as rating, r.movie_id as id
        FROM Reviews r
            JOIN People p ON r.user_id = p.person_id
        WHERE
            p.gender = 'male'
    ) m_r ON m.movie_id = m_r.id
GROUP BY
    m.movie_id;
