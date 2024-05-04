-- Active: 1709919509361@@127.0.0.1@5432@postgres@public

CREATE TABLE Movies (
    movie_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    duration INTERVAL,
    release_date DATE,
    remake_id INTEGER,
    FOREIGN KEY (remake_id) REFERENCES Movies(movie_id)
);

CREATE TABLE Genres (
    genre_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE MovieGenreConnecter (
    movie_id INTEGER,
    genre_id INTEGER,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
    FOREIGN KEY (genre_id) REFERENCES Genres(genre_id)
);

CREATE TABLE People (
    person_id SERIAL PRIMARY KEY,
    person_type VARCHAR(255) NOT NULL CHECK (
        person_type IN (
            'actor', 'composer', 'user'
        )
    ),
    name VARCHAR(255) NOT NULL,
    age INTEGER,
    gender VARCHAR(255) CHECK (
        gender IN ('male', 'female', 'attack helicopter')
    )
);

CREATE TABLE MovieActorConnecter (
    movie_id INTEGER,
    actor_id INTEGER,
    actor_role VARCHAR(255),
    PRIMARY KEY (movie_id, actor_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
    FOREIGN KEY (actor_id) REFERENCES People(person_id)
);

CREATE TABLE Soundtracks (
    soundtrack_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    release_date DATE,
    duration INTERVAL,
    movie_id INTEGER,
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

CREATE TABLE ComposerSoundtrackConnecter (
    soundtrack_id INTEGER,
    composer_id INTEGER,
    PRIMARY KEY (soundtrack_id, composer_id),
    FOREIGN KEY (soundtrack_id) REFERENCES Soundtracks(soundtrack_id),
    FOREIGN KEY (composer_id) REFERENCES People(person_id)
);

CREATE TABLE Awards (
    award_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    award_type VARCHAR(255) NOT NULL CHECK (
        award_type IN ('person', 'movie')
    )
);

CREATE TABLE AwardPersonConnecter (
    award_id INTEGER,
    person_id INTEGER,
    PRIMARY KEY (award_id, person_id),
    FOREIGN KEY (award_id) REFERENCES Awards(award_id),
    FOREIGN KEY (person_id) REFERENCES People(person_id)
);

CREATE TABLE AwardMovieConnecter (
    award_id INTEGER,
    movie_id INTEGER,
    PRIMARY KEY (award_id, movie_id),
    FOREIGN KEY (award_id) REFERENCES Awards(award_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id)
);

CREATE TABLE Reviews (
    movie_id INTEGER,
    contents TEXT,
    rating FLOAT CHECK (
        rating BETWEEN 0.0
        AND 10.0
    ),
    user_id INTEGER,
    PRIMARY KEY (movie_id, user_id),
    FOREIGN KEY (movie_id) REFERENCES Movies(movie_id),
    FOREIGN KEY (user_id) REFERENCES People(person_id)
);

CREATE TABLE ReviewsHistory (
    movie_id INTEGER,
    contents TEXT,
    rating FLOAT CHECK (
        rating BETWEEN 0.0
        AND 10.0
    ),
    date_added DATE NOT NULL,
    user_id INTEGER,
    PRIMARY KEY (movie_id, user_id, date_added),
    FOREIGN KEY (movie_id, user_id) REFERENCES Reviews(movie_id, user_id)
);
