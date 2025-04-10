# # from pyspark.sql import SparkSession
# # from pyspark.sql.functions import col, from_json, explode, regexp_replace
# # from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType

# # # Initialize Spark session
# # spark = SparkSession.builder \
# #     .appName("CryptoDataTransformation") \
# #     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2") \
# #     .config("spark.jars", "file:///C:/mysql/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0.jar") \
# #     .getOrCreate()

# # # Define schema for Kafka data
# # schema = ArrayType(
# #     StructType([
# #         StructField("id", StringType(), True),
# #         StructField("symbol", StringType(), True),
# #         StructField("name", StringType(), True),
# #         StructField("current_price", DoubleType(), True),
# #         StructField("market_cap", DoubleType(), True),
# #         StructField("total_volume", DoubleType(), True),
# #     ])
# # )

# # # Read data from Kafka
# # kafka_stream = spark.readStream \
# #     .format("kafka") \
# #     .option("kafka.bootstrap.servers", "localhost:9092") \
# #     .option("subscribe", "etl_topic") \
# #     .option("startingOffsets", "earliest") \
# #     .load()

# # # Parse and transform data
# # parsed_data = kafka_stream \
# #     .selectExpr("CAST(value AS STRING) as value") \
# #     .withColumn("cleaned_value", regexp_replace(col("value"), "^b'|'$", "")) \
# #     .withColumn("parsed_json", from_json(col("cleaned_value"), schema)) \
# #     .withColumn("cryptos", explode(col("parsed_json"))) \
# #     .select(
# #         col("cryptos.id").alias("id"),
# #         col("cryptos.symbol").alias("symbol"),
# #         col("cryptos.name").alias("name"),
# #         col("cryptos.current_price").alias("current_price"),
# #         col("cryptos.market_cap").alias("market_cap"),
# #         col("cryptos.total_volume").alias("total_volume")
# #     )

# # # Filter out invalid rows
# # filtered_data = parsed_data.filter(col("id").isNotNull()).dropDuplicates()

# # # Write data to MySQL
# # def write_to_mysql(batch_df, batch_id):
# #     print(f"Processing Batch ID: {batch_id}")
# #     batch_df.show(truncate=False)
# #     try:
# #         batch_df.write.jdbc(
# #             url="jdbc:mysql://localhost:3306/crypto_data",
# #             table="crypto_data",
# #             mode="append",
# #             properties={
# #                 "user": "root",
# #                 "password": "root",
# #                 "driver": "com.mysql.cj.jdbc.Driver"
# #             }
# #         )
# #         print(f"Batch {batch_id} successfully written to MySQL.")
# #     except Exception as e:
# #         print(f"Failed to write batch {batch_id} to MySQL: {e}")

# # query = filtered_data.writeStream \
# #     .foreachBatch(write_to_mysql) \
# #     .outputMode("append") \
# #     .start()

# # query.awaitTermination()

# from pyspark.sql import SparkSession
# from pyspark.sql.functions import col, from_json, explode, regexp_replace, current_timestamp
# from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType

# # Initialize Spark session
# spark = SparkSession.builder \
#     .appName("CryptoDataTransformation") \
#     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2") \
#     .config("spark.jars", "file:///C:/mysql/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0.jar") \
#     .getOrCreate()

# # Define schema for Kafka data
# schema = ArrayType(
#     StructType([
#         StructField("id", StringType(), True),
#         StructField("symbol", StringType(), True),
#         StructField("name", StringType(), True),
#         StructField("current_price", DoubleType(), True),
#         StructField("market_cap", DoubleType(), True),
#         StructField("total_volume", DoubleType(), True),
#     ])
# )

# # Read data from Kafka
# kafka_stream = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "localhost:9092") \
#     .option("subscribe", "etl_topic") \
#     .option("startingOffsets", "earliest") \
#     .load()

# # Parse and transform data
# parsed_data = kafka_stream \
#     .selectExpr("CAST(value AS STRING) as value") \
#     .withColumn("cleaned_value", regexp_replace(col("value"), "^b'|'$", "")) \
#     .withColumn("parsed_json", from_json(col("cleaned_value"), schema)) \
#     .withColumn("cryptos", explode(col("parsed_json"))) \
#     .select(
#         col("cryptos.id").alias("ID"),
#         col("cryptos.symbol").alias("SYMBOL"),
#         col("cryptos.name").alias("NAME"),
#         col("cryptos.current_price").alias("CURRENT_PRICE"),
#         col("cryptos.market_cap").alias("MARKET_CAP"),
#         col("cryptos.total_volume").alias("TOTAL_VOLUME")
#     ) \
#     .withColumn("LAST_UPDATED", current_timestamp())  # Add timestamp column

# # Ensure data consistency by filtering out null values
# filtered_data = parsed_data.filter(col("ID").isNotNull())

# # Write data to MySQL (UPSERT logic)
# def write_to_mysql(batch_df, batch_id):
#     print(f"Processing Batch ID: {batch_id}")
#     batch_df.show(truncate=False)

#     # Define MySQL connection properties
#     mysql_url = "jdbc:mysql://localhost:3306/crypto_data"
#     properties = {
#         "user": "root",
#         "password": "root",
#         "driver": "com.mysql.cj.jdbc.Driver"
#     }

#     try:
#         # Read existing data from MySQL
#         existing_df = spark.read.jdbc(mysql_url, "crypto_data", properties=properties)
        
#         # Merge new data with existing records (UPSERT)
#         merged_df = batch_df.alias("new").join(
#             existing_df.alias("old"),
#             batch_df["ID"] == existing_df["ID"],
#             "left"
#         ).select(
#             batch_df["ID"],
#             batch_df["SYMBOL"],
#             batch_df["NAME"],
#             batch_df["CURRENT_PRICE"],
#             batch_df["MARKET_CAP"],
#             batch_df["TOTAL_VOLUME"],
#             batch_df["LAST_UPDATED"]
#         )

#         # Write updated data to MySQL
#         merged_df.write.jdbc(
#             url=mysql_url,
#             table="crypto_data",
#             mode="overwrite",  # Overwrite table to update values
#             properties=properties
#         )

#         print(f"Batch {batch_id} successfully written to MySQL.")

#     except Exception as e:
#         print(f"Failed to write batch {batch_id} to MySQL: {e}")

# # Streaming query to write data into MySQL
# query = filtered_data.writeStream \
#     .foreachBatch(write_to_mysql) \
#     .outputMode("append") \
#     .start()

# query.awaitTermination()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, explode, regexp_replace, current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType

# Initialize Spark session
# Creates a SparkSession named "CryptoDataTransformation"
# Loads Kafka connector (spark-sql-kafka) for streaming data from Kafka.
# Loads MySQL JDBC driver (mysql-connector-j-9.0.0.jar) for writing data to MySQL
spark = SparkSession.builder \
    .appName("CryptoDataTransformation") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2") \
    .config("spark.jars", "file:///C:/mysql/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0.jar") \
    .getOrCreate()

# Define schema for Kafka data
# Defines the schema for parsing JSON messages received from Kafka.
# The data is an array of objects, so we use ArrayType(StructType([...])).
schema = ArrayType(
    StructType([
        StructField("id", StringType(), True),
        StructField("symbol", StringType(), True),
        StructField("name", StringType(), True),
        StructField("current_price", DoubleType(), True),
        StructField("market_cap", DoubleType(), True),
        StructField("total_volume", DoubleType(), True)
    ])
)

# Reads a real-time data stream from Kafka topic: "etl_topic".
# startingOffsets: earliest means it starts consuming messages from the beginning
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "etl_topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse and transform data
# 223 Extracts the Kafka message (value) as a string.
# 224 Cleans the string (regexp_replace) to remove unwanted characters (b' and ').
# 225 Parses the cleaned string into JSON format (from_json(...)).
# 226 Expands (explode) the JSON array into multiple rows.
# 227-234 Extracts relevant columns and adds a timestamp (last_updated).
parsed_data = kafka_stream \
    .selectExpr("CAST(value AS STRING) as value") \
    .withColumn("cleaned_value", regexp_replace(col("value"), "^b'|'$", "")) \
    .withColumn("parsed_json", from_json(col("cleaned_value"), schema)) \
    .withColumn("cryptos", explode(col("parsed_json"))) \
    .select(
        col("cryptos.id").alias("id"),
        col("cryptos.symbol").alias("symbol"),
        col("cryptos.name").alias("name"),
        col("cryptos.current_price").alias("current_price"),
        col("cryptos.market_cap").alias("market_cap"),
        col("cryptos.total_volume").alias("total_volume"),
        current_timestamp().alias("last_updated")
    )

# Removes rows with missing IDs (filter(col("id").isNotNull()))
# Removes duplicate records based on the id column (dropDuplicates(["id"]))
filtered_data = parsed_data.filter(col("id").isNotNull()).dropDuplicates(["id"])

# This function writes each batch of processed data into MySQL.
# Uses the JDBC connection to connect to MySQL database crypto_data.
# Mode: "overwrite" replaces the existing table (can be changed to "append").
# If batch writing fails, it catches and prints the error.
def upsert_to_mysql(batch_df, batch_id):
    print(f"Processing Batch ID: {batch_id}")
    batch_df.show(truncate=False)
    try:
        batch_df.write.jdbc(
            url="jdbc:mysql://localhost:3306/crypto_data",
            table="crypto_data",
            mode="overwrite",
            properties={
                "user": "root",
                "password": "root",
                "driver": "com.mysql.cj.jdbc.Driver"
            }
        )
        print(f"Batch {batch_id} successfully written to MySQL.")
    except Exception as e:
        print(f"Failed to write batch {batch_id} to MySQL: {e}")
        
# Processes the filtered data in micro-batches (foreachBatch(upsert_to_mysql)).
# Runs the upsert function on each batch.
# Keeps the streaming job running (awaitTermination()).
query = filtered_data.writeStream \
    .foreachBatch(upsert_to_mysql) \
    .outputMode("append") \
    .start()

query.awaitTermination()
