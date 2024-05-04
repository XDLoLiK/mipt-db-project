-- Сделаем индексы для фильмов, потому что их названия часто ищут
CREATE INDEX ON Movies (title);

-- Также создадим индекс для имён людей
CREATE INDEX ON People (name);

-- Создадим индекс для отзывов по конкретному фильму
CREATE INDEX ON Reviews (movie_id);

-- Историю отзывов отсортируем по дате
CREATE INDEX ON ReviewsHistory (date_added DESC);
