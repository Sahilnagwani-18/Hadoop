from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegressionModel
import json

spark = SparkSession.builder \
    .appName("ExportLRModel") \
    .master("local[*]") \
    .getOrCreate()

# Load model from LOCAL filesystem
model = LogisticRegressionModel.load("file:///home/user/logistic_genre_model")

# Multinomial Logistic Regression → coefficientMatrix
coef_matrix = model.coefficientMatrix.toArray().tolist()
intercepts = model.interceptVector.toArray().tolist()

num_classes = model.numClasses
num_features = model.numFeatures

genre_labels = [
    "Crime", "Romance", "Thriller", "Adventure", "Drama", "War", "Documentary",
    "Fantasy", "Mystery", "Musical", "Animation", "Film-Noir",
    "(no genres listed)", "IMAX", "Horror", "Western", "Comedy",
    "Children", "Action", "Sci-Fi"
]

model_data = {
    "coefficient_matrix": coef_matrix,   # shape: [num_classes x num_features]
    "intercepts": intercepts,            # length = num_classes
    "num_classes": num_classes,
    "num_features": num_features,
    "labels": genre_labels
}

with open("lr_model_export.json", "w") as f:
    json.dump(model_data, f, indent=4)

print("Exported → lr_model_export.json")

spark.stop()

