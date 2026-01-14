from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower
from pyspark.ml import PipelineModel

spark = SparkSession.builder \
    .appName("PredictGenre") \
    .getOrCreate()

model = PipelineModel.load("hdfs://master:9000/models/genre_model")

def predict_genre(title):
    df = spark.createDataFrame([[title]], ["Movie_Name"])
    df = df.withColumn("Title_Clean", lower(col("Movie_Name")))
    out = model.transform(df).collect()[0]
    return out["prediction"]

