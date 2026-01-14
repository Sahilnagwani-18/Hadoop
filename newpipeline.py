from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, lower, regexp_replace
from pyspark.ml.feature import RegexTokenizer, HashingTF, StringIndexer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator

spark = SparkSession.builder \
    .appName("Lightweight Logistic Regression Movie Genre Classifier") \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "4g") \
    .config("spark.memory.fraction", "0.4") \
    .getOrCreate()

print("Spark started!")

# ===================== LOAD DATA =====================
df = spark.read.csv(
    "hdfs://master:9000/movies/movies_clean.csv",
    header=True,
    inferSchema=True
).select("Movie_Name", "Genre")

df = df.withColumn(
    "Title_Clean",
    lower(regexp_replace("Movie_Name", "[^a-zA-Z0-9 ]", " "))
)

# Take only first genre
df = df.withColumn("Genre_Main", split(col("Genre"), "\\|")[0])

# ===================== LABEL ENCODING =====================
label_indexer = StringIndexer(inputCol="Genre_Main", outputCol="label")
df = label_indexer.fit(df).transform(df)

# ===================== TEXT PROCESSING =====================
tokenizer = RegexTokenizer(
    inputCol="Title_Clean",
    outputCol="tokens",
    pattern="\\W+"
)
df = tokenizer.transform(df)

tf = HashingTF(
    inputCol="tokens",
    outputCol="features",
    numFeatures=2000   # More features for better accuracy
)
df = tf.transform(df)

# ===================== TRAIN / TEST SPLIT =====================
train, test = df.randomSplit([0.8, 0.2], seed=42)

# ===================== LOGISTIC REGRESSION =====================
lr = LogisticRegression(
    featuresCol="features",
    labelCol="label",
    maxIter=30,
    regParam=0.01,
    elasticNetParam=0.0  # pure L2 (best for text)
)

print("Training Logistic Regression...")
lr_model = lr.fit(train)

# ===================== SAVE MODEL =====================
lr_model.write().overwrite().save("hdfs://master:9000/models/logistic_genre_model")
print("Model saved to HDFS at /models/logistic_genre_model")

# ===================== EVALUATE =====================
pred = lr_model.transform(test)

evaluator = MulticlassClassificationEvaluator(
    labelCol="label",
    predictionCol="prediction",
    metricName="accuracy"
)

accuracy = evaluator.evaluate(pred)
print("Accuracy =", accuracy)

spark.stop()

