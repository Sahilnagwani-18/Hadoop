from pyspark.sql import SparkSession
from pyspark.sql.functions import col, split, explode, lower, regexp_replace, array_contains, rand
from pyspark.ml import Pipeline
from pyspark.ml.feature import RegexTokenizer, StopWordsRemover, HashingTF, IDF
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.util import MLWritable
import builtins   # To use Python's sum()

# ----------------------------------------------------------
# Spark Session
# ----------------------------------------------------------
spark = SparkSession.builder \
    .appName("Movie Genre MultiLabel - KFold") \
    .config("spark.driver.memory", "6g") \
    .config("spark.executor.memory", "6g") \
    .config("spark.executor.cores", "2") \
    .config("spark.sql.shuffle.partitions", "8") \
    .getOrCreate()

print("\n### Spark Started ###\n")

# ----------------------------------------------------------
# Load Data
# ----------------------------------------------------------
df = spark.read.csv("hdfs://master:9000/movies/movies_clean.csv",
                    header=True, inferSchema=True) \
               .select("Movie_Name", "Genre")

df = df.withColumn("Title_Clean",
                   lower(regexp_replace("Movie_Name", "[^a-zA-Z0-9 ]", " ")))
df = df.withColumn("Genre_Array", split(col("Genre"), "\\|"))

# Extract all unique genres
all_genres = (
    df.select(explode(col("Genre_Array")).alias("g"))
      .filter(col("g") != "")
      .distinct()
)
genre_list = [r["g"] for r in all_genres.collect()]
print("\nUnique Genres:", genre_list)

# Assign folds
K = 5
df = df.withColumn("fold", (rand() * K).cast("int"))

df.cache()
print("Total rows =", df.count())

# ----------------------------------------------------------
# Text processing pipeline (shared)
# ----------------------------------------------------------
tokenizer = RegexTokenizer(inputCol="Title_Clean", outputCol="tokens", pattern="\\W+")
stop_remove = StopWordsRemover(inputCol="tokens", outputCol="filtered")
tf = HashingTF(inputCol="filtered", outputCol="tf_raw", numFeatures=8000)
idf = IDF(inputCol="tf_raw", outputCol="features")

text_pipeline = Pipeline(stages=[tokenizer, stop_remove, tf, idf])
text_model = text_pipeline.fit(df)
df = text_model.transform(df)

# SAVE PREPROCESSING PIPELINE
text_model.save("hdfs://master:9000/models/text_pipeline")

# ----------------------------------------------------------
# Train & Evaluate — One Logistic Regression per genre
# ----------------------------------------------------------
results = {}

for genre in genre_list:
    print(f"\n============================")
    print(f" Training genre: {genre}")
    print(f"============================")

    # Binary label: 1 if movie contains this genre
    df_g = df.withColumn("label", array_contains(col("Genre_Array"), genre).cast("int"))

    genre_scores = []

    for fold_id in range(K):
        print(f"\n### Fold {fold_id+1}/{K} ###")

        train_df = df_g.filter(col("fold") != fold_id)
        test_df  = df_g.filter(col("fold") == fold_id)

        print("Train rows:", train_df.count())
        print("Test rows:", test_df.count())

        lr = LogisticRegression(maxIter=40, featuresCol="features", labelCol="label")
        model = lr.fit(train_df)

        preds = model.transform(test_df)

        evaluator = BinaryClassificationEvaluator(labelCol="label", rawPredictionCol="rawPrediction")
        score = evaluator.evaluate(preds)

        print(f"Fold F1 = {score}")
        genre_scores.append(score)

    # Calculate average score safely
    avg_score = builtins.sum(genre_scores) / len(genre_scores)
    results[genre] = avg_score

    print(f"\nAverage score for {genre} = {avg_score}")

    # SAVE MODEL FOR THIS GENRE
    model_path = f"hdfs://master:9000/models/logreg_{genre}"
    model.save(model_path)
    print(f"Saved model: {model_path}")

# ----------------------------------------------------------
# Save final results to HDFS
# ----------------------------------------------------------
from pyspark.sql import Row
results_df = spark.createDataFrame([Row(genre=g, f1=float(s)) for g, s in results.items()])
results_df.write.mode("overwrite").csv("hdfs://master:9000/models/final_genre_scores")

print("\nResults saved at: hdfs://master:9000/models/final_genre_scores")

# ----------------------------------------------------------
# Print final results locally
# ----------------------------------------------------------
print("\n\n====== FINAL GENRE SCORES ======")
for g, s in results.items():
    print(g, "=", s)

spark.stop()

