from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CryptoDataTransformation") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2") \
    .config("spark.jars", "C:\mysql\mysql-connector-j-9.0.0\mysql-connector-j-9.0.0\mysql-connector-j-9.0.0.jar") \
    .getOrCreate()

# Define schema for the Kafka data
schema = StructType([
    StructField("id", StringType(), False),
    StructField("symbol", StringType(), True),
    StructField("name", StringType(), True),
    StructField("current_price", DoubleType(), True),
    StructField("market_cap", DoubleType(), True),
    StructField("total_volume", DoubleType(), True)
])

# Read data from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "etl_topic") \
    .load() \
    .selectExpr("CAST(value AS STRING) as json_value") \
    .select(from_json(col("json_value"), schema).alias("data")) \
    .select("data.*")

# Function to write DataFrame to MySQL
def write_to_mysql(batch_df, batch_id):
    print("Batch ID:", batch_id)
    # Debugging: Show the first few rows of the DataFrame
    print("Batch Data:")
    batch_df.show(truncate=False)
    
    # Check schema
    print("Schema:")
    batch_df.printSchema()

    # Ensure the DataFrame columns match the MySQL table schema
    batch_df = batch_df.select(
        col("id"),
        col("symbol"),
        col("name"),
        col("current_price"),
        col("market_cap"),
        col("total_volume")
    )

    # Write DataFrame to MySQL
    try:
        batch_df.write.jdbc(
            url="jdbc:mysql://localhost:3306/crypto_data",
            table="crypto_data",
            mode="append",
            properties={
                "user": "root",
                "password": "root",
                "driver": "com.mysql.cj.jdbc.Driver"
            }
        )
    except Exception as e:
        print(f"Failed to write batch {batch_id} to MySQL: {e}")

# Write stream to MySQL
query = df.writeStream \
    .foreachBatch(write_to_mysql) \
    .outputMode("append") \
    .start()

# Await termination
query.awaitTermination()