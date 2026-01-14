from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StringIndexer
from pyspark.ml.regression import LinearRegression
from pyspark.sql.functions import col

# ✅ Step 1: Initialize Spark Session
spark = SparkSession.builder \
    .appName("PySpark Linear Regression - Housing Data") \
    .master("spark://master:7077") \
    .getOrCreate()

print("\n✅ Spark Session started successfully!\n")

# ✅ Step 2: Load the dataset from HDFS or local path
# If your file is uploaded to HDFS: use 'hdfs://master:9000/input/Housing.csv'
# If local on master node:
df = spark.read.csv("Housing.csv", header=True, inferSchema=True)

print("✅ Dataset loaded successfully!")
df.printSchema()
print(f"Total Rows: {df.count()}")

# ✅ Step 3: Convert categorical boolean columns to numeric
bool_cols = ["mainroad", "guestroom", "basement", "hotwaterheating", "airconditioning"]

for col_name in bool_cols:
    indexer = StringIndexer(inputCol=col_name, outputCol=col_name + "_double")
    df = indexer.fit(df).transform(df)

# ✅ Step 4: Drop any rows with missing/null values
df = df.na.drop()
print(f"✅ Cleaned data (nulls removed). Rows after cleaning: {df.count()}")

# ✅ Step 5: Define feature columns
feature_cols = [
    "area", "bedrooms", "bathrooms", "stories",
    "mainroad_double", "guestroom_double", "basement_double",
    "hotwaterheating_double", "airconditioning_double"
]

# ✅ Step 6: Create feature vector
assembler = VectorAssembler(
    inputCols=feature_cols,
    outputCol="features",
    handleInvalid="skip"  # Prevents null-related errors
)

df_vector = assembler.transform(df).select(col("features"), col("price").alias("label"))

# ✅ Step 7: Split into training and test sets
train, test = df_vector.randomSplit([0.8, 0.2], seed=42)
print(f"✅ Training set: {train.count()} rows | Test set: {test.count()} rows")

# ✅ Step 8: Initialize and train Linear Regression model
lr = LinearRegression(featuresCol="features", labelCol="label")
model = lr.fit(train)

# ✅ Step 9: Evaluate the model
predictions = model.transform(test)
predictions.select("features", "label", "prediction").show(10, truncate=False)

# ✅ Step 10: Print model coefficients and metrics
print("\n===== Linear Regression Model Summary =====")
print(f"Coefficients: {model.coefficients}")
print(f"Intercept: {model.intercept}")

summary = model.summary
print(f"RMSE: {summary.rootMeanSquaredError}")
print(f"R²: {summary.r2}")
print("===========================================\n")

# ✅ Step 11: Stop Spark session
spark.stop()
print("✅ Spark session stopped successfully.")

