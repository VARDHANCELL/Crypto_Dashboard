from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, unbase64
from pyspark.sql.types import StructType, StructField, StringType

# Define the schema for the JSON data
schema = StructType([
    StructField("id", StringType(), True),
    StructField("symbol", StringType(), True),
    StructField("name", StringType(), True),
    StructField("current_price", StringType(), True),
    StructField("market_cap", StringType(), True),
    StructField("total_volume", StringType(), True),
    # Add more fields as needed
])

# Initialize Spark session
spark = SparkSession.builder \
    .appName("KafkaSparkStreamingConsumer") \
    .config("spark.sql.streaming.kafka.version", "3.0.0") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0") \
    .getOrCreate()

# Define Kafka stream
kafkaStreamDF = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "etl_topic") \
    .load()

# Process data
processedDF = kafkaStreamDF.selectExpr("CAST(value AS STRING)") \
    .withColumn("json_data", from_json(col("value"), schema)) \
    .select("json_data.*")  # Flatten the JSON data by selecting all fields
    
# Example: Print processed data to console (for debugging)
query = processedDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Await termination of the stream (useful for debugging, remove in production)
query.awaitTermination()