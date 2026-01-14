from pyspark import SparkConf, SparkContext

conf = SparkConf()
conf.setAppName("PySparkClusterTest")
conf.setMaster("spark://master:7077")

sc = SparkContext(conf=conf)

# Simple distributed operation
data = list(range(1, 100001))
rdd = sc.parallelize(data, numSlices=4)  # 4 partitions
result = rdd.map(lambda x: x * x).sum()

print("✅ PySpark Distributed Sum of Squares:", result)

# Check which nodes executed tasks
print("Executors:", sc._jsc.sc().statusTracker().getExecutorInfos())

sc.stop()

