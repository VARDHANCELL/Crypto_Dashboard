# Crypto_Dashboard

## Project Overview:

This project builds an ETL (Extract, Transform, Load) pipeline to process real-time cryptocurrency data. The pipeline fetches live data using Kafka producers, processes and transforms it using Apache Spark, stores it in MySQL, and visualizes it using Power BI.

## Features:

    1. Real-Time Data Streaming:

        Fetches live cryptocurrency data from APIs.
        Streams data using Kafka producers and consumers.
        
    2. Data Transformation:

        Filters and processes the top 100 cryptocurrencies by market cap.
        Updates existing records in MySQL or inserts new ones (Upsert functionality).
        Tracks the processing date and time.
        
    3. Data Visualization:

        Provides insightful analytics on cryptocurrency trends using Power BI dashboards.
        
## Technologies Used:

    1. Apache Kafka: For data ingestion and real-time streaming.
    2. Apache Spark: For data transformation and real-time processing.
    3. MySQL: For storing transformed data in a relational database.
    4. Power BI: For visualizing cryptocurrency trends and metrics.
    5. Python: For scripting the producer, consumer, and transformation logic.
    
## Setup Instructions:

    1. Prerequisites
        Java 8 or later
        Apache Kafka (v3.5.2 or compatible)
        Apache Spark (v3.5.2 with Hadoop 3 support)
        MySQL (v8 or later)
        Python 3.8 or later
        Power BI Desktop
        
    2. Installation Steps
        Step 1: Setup Kafka
            Download and extract Kafka.
            Start Zookeeper:
                bash~zookeeper-server-start.bat config\zookeeper.properties
            Start Kafka broker:
                bash~kafka-server-start.bat config\server.properties
            Create a Kafka topic:
                bash~kafka-topics.bat --create --topic etl_topic --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1
                
        Step 2: Setup MySQL
            Create a database:
                sql~CREATE DATABASE crypto_data;
            Create a table:
                sql~CREATE TABLE crypto_data (
                    id VARCHAR(50) PRIMARY KEY,
                    symbol VARCHAR(10),
                    name VARCHAR(100),
                    current_price DOUBLE,
                    market_cap DOUBLE,
                    total_volume DOUBLE,
                    processed_at DATETIME);
                    
        Step 3: Setup Spark
            Install Apache Spark and set the environment variables (SPARK_HOME, PATH).
            Install the necessary packages:
                bash~pip install pyspark
            Download the MySQL Connector JAR and place it in the project directory.

        Step 4: Run the Scripts
            Start the Kafka producer:
                bash~python kafka_producer.py
            Start the Spark transformation script:
                bash~spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2 \
                   --jars path/to/mysql-connector-java.jar \
                     data_transformation.py
                     
        Step 5: Power BI Visualization
            Connect Power BI to MySQL.
            Create visualizations to display:
            Cryptocurrency trends.
            Market caps and prices of the top 100 coins.
            Real-time updates with the processed_at timestamp.

## Future Improvements:
Add more data sources for diversified cryptocurrency insights.
Integrate advanced analytics like price prediction using machine learning.
Deploy the pipeline on cloud platforms (AWS/GCP/Azure).

## Contributors:
Harshvardhan - Developer
Feel free to contribute by raising issues or submitting pull requests.
If you have any doubt please let me know at harshvardhan28101@gmail.com

## License
This project is licensed under the MIT License. See the LICENSE file for details.
