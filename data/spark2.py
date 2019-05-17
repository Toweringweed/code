from pyspark.sql import SparkSession
spark = SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()

sc = spark.sparkContext

spark.createDataFrame(sc.parallelize(range(1, 6)).map(lambda i: Row(single=i, double=i ** 2))).collect()
