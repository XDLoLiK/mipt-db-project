-- Функция, возвращающая количество наград у какого-то фильма
CREATE OR REPLACE FUNCTION award_count(id INT) RETURNS DECIMAL 
AS 
$$
BEGIN
	RETURN (
	    SELECT COUNT(a.award_id) as awards_amount
	    FROM
	        Movies m
	        JOIN AwardMovieConnecter a_m ON m.movie_id = a_m.movie_id
	        JOIN Awards a ON a.award_id = a_m.award_id
	    GROUP BY
	        m.movie_id
	    HAVING
	        m.movie_id = id
	);
END;
$$
LANGUAGE
PLPGSQL; 

SELECT * FROM award_count (5);

-- Функция, возвращающая таблицу фильмов, рейтинг которых находится в каком-то промежутке
CREATE OR REPLACE FUNCTION movies_in_range(rating_from FLOAT, 
rating_to FLOAT) RETURNS TABLE(title VARCHAR(255)) AS 
$$
BEGIN
	RETURN QUERY
	SELECT m.title
	FROM Movies m
	    JOIN Reviews r ON r.movie_id = m.movie_id
	GROUP BY
	    m.movie_id
	HAVING
	    ROUND(AVG(r.rating)) BETWEEN rating_from and rating_to;
END;
$$
LANGUAGE
PLPGSQL; 

SELECT * FROM movies_in_range (5, 10);

-- Функция, возвращающая названия фильмов, вышедших не раньше указанной даты
CREATE OR REPLACE FUNCTION new_movies(release DATE) RETURNS TABLE
(name VARCHAR(255)) AS 
$$
BEGIN
	RETURN QUERY
	SELECT title
	FROM Movies
	WHERE
	    release_date >= release;
END;
$$
LANGUAGE
PLPGSQL; 

SELECT * FROM new_movies ('06-17-2013');
