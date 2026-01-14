-- ==========================================================
--  FINAL BIG DATA ANALYTICS SCRIPT FOR MOVIE DATASET (HIVE)
--  Author: Sahil Nagwani
-- ==========================================================


-- ================================
-- STEP 0: REMOVE OLD TABLES
-- ================================

DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS genre_avg_rating;
DROP TABLE IF EXISTS genre_popularity;
DROP TABLE IF EXISTS top_users;
DROP TABLE IF EXISTS movie_popularity;
DROP TABLE IF EXISTS top_rated_movies;
DROP TABLE IF EXISTS genre_distribution;


-- ==========================================================
-- STEP 1: CREATE MOVIES TABLE USING OpenCSVSerde
-- ==========================================================

CREATE TABLE movies (
    user_id INT,
    movie_name STRING,
    rating FLOAT,
    genre STRING
)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
    "separatorChar" = ",",
    "quoteChar"     = "\"",
    "escapeChar"    = "\\"
)
STORED AS TEXTFILE
TBLPROPERTIES ("skip.header.line.count"="1");


-- ==========================================================
-- STEP 2: LOAD DATA FROM HDFS
-- ==========================================================

LOAD DATA INPATH '/movies/movies_clean.csv'
INTO TABLE movies;
-- NOTE: Using INTO TABLE avoids deleting the source file.


-- ==========================================================
-- STEP 3: ANALYTICS QUERIES
-- ==========================================================


-- 3.1 AVERAGE RATING PER GENRE
DROP TABLE IF EXISTS genre_avg_rating;
CREATE TABLE genre_avg_rating AS
SELECT genre, AVG(rating) AS avg_rating
FROM movies
GROUP BY genre
ORDER BY avg_rating DESC;


-- 3.2 GENRE POPULARITY (COUNT OF RATINGS)
DROP TABLE IF EXISTS genre_popularity;
CREATE TABLE genre_popularity AS
SELECT genre, COUNT(*) AS rating_count
FROM movies
GROUP BY genre
ORDER BY rating_count DESC;


-- 3.3 TOP USERS (MOST ACTIVE USERS)
DROP TABLE IF EXISTS top_users;
CREATE TABLE top_users AS
SELECT user_id, COUNT(*) AS ratings_given
FROM movies
GROUP BY user_id
ORDER BY ratings_given DESC
LIMIT 20;


-- 3.4 MOVIE POPULARITY (MOST RATED MOVIES)
DROP TABLE IF EXISTS movie_popularity;
CREATE TABLE movie_popularity AS
SELECT movie_name, COUNT(*) AS rating_count
FROM movies
GROUP BY movie_name
ORDER BY rating_count DESC
LIMIT 20;


-- 3.5 TOP RATED MOVIES (MINIMUM 20 RATINGS)
DROP TABLE IF EXISTS top_rated_movies;
CREATE TABLE top_rated_movies AS
SELECT movie_name, AVG(rating) AS avg_rating, COUNT(*) AS total_ratings
FROM movies
GROUP BY movie_name
HAVING COUNT(*) > 20
ORDER BY avg_rating DESC
LIMIT 20;


-- 3.6 GENRE DISTRIBUTION
DROP TABLE IF EXISTS genre_distribution;
CREATE TABLE genre_distribution AS
SELECT genre, COUNT(*) AS count
FROM movies
GROUP BY genre
ORDER BY count DESC;


-- ==========================================================
-- STEP 4: SUMMARY MESSAGE
-- ==========================================================

SELECT "✔ Hive analytics completed successfully!" AS status;
SELECT "✔ Result tables created:" AS message;

SELECT "   → genre_avg_rating" AS tables;
SELECT "   → genre_popularity" AS tables;
SELECT "   → top_users" AS tables;
SELECT "   → movie_popularity" AS tables;
SELECT "   → top_rated_movies" AS tables;
SELECT "   → genre_distribution" AS tables;


