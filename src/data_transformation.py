from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, explode, regexp_replace
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, ArrayType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CryptoDataTransformation") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2") \
    .config("spark.jars", "file:///C:/mysql/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0.jar") \
    .getOrCreate()

# Define schema for Kafka data
schema = ArrayType(
    StructType([
        StructField("id", StringType(), True),
        StructField("symbol", StringType(), True),
        StructField("name", StringType(), True),
        StructField("current_price", DoubleType(), True),
        StructField("market_cap", DoubleType(), True),
        StructField("total_volume", DoubleType(), True),
    ])
)

# Read data from Kafka
kafka_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "etl_topic") \
    .option("startingOffsets", "earliest") \
    .load()

# Parse and transform data
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
        col("cryptos.total_volume").alias("total_volume")
    )

# Filter out invalid rows
filtered_data = parsed_data.filter(col("id").isNotNull()).dropDuplicates()

# Write data to MySQL
def write_to_mysql(batch_df, batch_id):
    print(f"Processing Batch ID: {batch_id}")
    batch_df.show(truncate=False)
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
        print(f"Batch {batch_id} successfully written to MySQL.")
    except Exception as e:
        print(f"Failed to write batch {batch_id} to MySQL: {e}")

query = filtered_data.writeStream \
    .foreachBatch(write_to_mysql) \
    .outputMode("append") \
    .start()

query.awaitTermination()
