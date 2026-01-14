from pyspark import SparkContext, SparkConf

# Configure Spark
conf = SparkConf().setAppName("WordCount").setMaster("yarn")
sc = SparkContext(conf=conf)

# Read input file from HDFS
text_file = sc.textFile("hdfs://master:9000/input/wordcount.txt")

# Transformations: split → map → reduce
counts = (text_file
          .flatMap(lambda line: line.split(" "))
          .map(lambda word: (word, 1))
          .reduceByKey(lambda a, b: a + b))

# Save output to HDFS
counts.saveAsTextFile("hdfs://master:9000/output/wordcount")

# Print top results in console
for word, count in counts.collect():
    print(f"{word}: {count}")

sc.stop()

