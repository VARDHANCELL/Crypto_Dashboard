from pyspark.sql import SparkSession # Main entry point for Spark functionality.
from pyspark.sql.functions import from_json, col # from_json:Converts a JSON string into a Spark DataFrame. col:Used to select and manipulate DataFrame columns.
from pyspark.sql.types import StructType, StructField, StringType, DoubleType # Define the schema of the incoming JSON data.

# Define the schema for the JSON data
# Defines how kafka msgs are structured
# True means the feild can be nullable
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
# Specifies dependencies required for Kafka-Spark integration using .config
spark = SparkSession.builder \
    .appName("KafkaSparkStreamingConsumer") \
    .config("spark.sql.streaming.kafka.version", "3.0.0") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.0.0") \
    .getOrCreate()

# Define Kafka stream
# Reads data from Kafka topic "etl_topic"
# Uses Kafka's bootstrap server running on localhost:9092
# readStream means this is a real-time streaming application
kafkaStreamDF = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "etl_topic") \
    .load()

# Process data
# Extracts the Kafka message value and converts it to a JSON object using from_json()
processedDF = kafkaStreamDF.selectExpr("CAST(value AS STRING)") \
    .withColumn("json_data", from_json(col("value"), schema)) \
    .select("json_data.*")  # select("json_data.*") flattens the JSON structure, so each field is accessible as a column
    
# Outputs processed data in append mode (new data gets added continuously)
query = processedDF.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

# Ensures that the streaming job keeps running until manually stopped.
query.awaitTermination()