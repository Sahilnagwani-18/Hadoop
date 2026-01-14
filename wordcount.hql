-- DROP old tables (optional but recommended)
DROP TABLE IF EXISTS wc_lines;
DROP TABLE IF EXISTS wc_words;
DROP TABLE IF EXISTS wc_result;

-- Load sample file
CREATE TABLE wc_lines (line STRING);

LOAD DATA INPATH '/hello_hive_input/sample.txt' INTO TABLE wc_lines;

-- Split into words
CREATE TABLE wc_words AS
SELECT explode(split(line, ' ')) AS word
FROM wc_lines;

-- Count words
CREATE TABLE wc_result AS
SELECT word, COUNT(*) AS count
FROM wc_words
GROUP BY word
ORDER BY count DESC;

SELECT * FROM wc_result;

