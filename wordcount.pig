
lines = LOAD '/input/sample.txt' AS (line:chararray);

words = FOREACH lines GENERATE FLATTEN(TOKENIZE(line)) AS word;

grouped = GROUP words BY word;

-- Count the number of occurrences for each word
wordcount = FOREACH grouped GENERATE group AS word, COUNT(words) AS count;

-- Store the result back into HDFS
STORE wordcount INTO '/pig_output110' USING PigStorage('\t');

