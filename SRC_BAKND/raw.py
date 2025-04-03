from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, expr
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Define the schema for the JSON data
schema = StructType([
    StructField("id", StringType(), True),
    StructField("symbol", StringType(), True),
    StructField("name", StringType(), True),
    StructField("current_price", DoubleType(), True),
    StructField("market_cap", DoubleType(), True),
    StructField("total_volume", DoubleType(), True),
    # Add more fields as needed
])

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkStreamingConsumer") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2") \
    .getOrCreate()

# Define Kafka stream
kafkaStreamDF = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "etl_topic") \
    .load()

# Process data
rawDF = kafkaStreamDF.selectExpr("CAST(value AS STRING)").alias("raw_data")
processedDF = rawDF \
    .withColumn("json_data", from_json(col("value"), schema)) \
    .select("json_data.*")  # Flatten the JSON data by selecting all fields

# Define a query to write raw data to the console
rawQuery = rawDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

# Define a query to write processed data to the console
processedQuery = processedDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .option("truncate", False) \
    .start()

# Await termination of the streams (useful for debugging, remove in production)
rawQuery.awaitTermination()
processedQuery.awaitTermination()
