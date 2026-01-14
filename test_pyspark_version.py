from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("PythonCheck").getOrCreate()

print("Python used by Spark executors:", spark.sparkContext.pythonExec)
print("Python used by Spark driver:", spark.sparkContext.pythonVer)

spark.stop()
