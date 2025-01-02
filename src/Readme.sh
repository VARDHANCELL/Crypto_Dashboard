# Zookeper command - 
    .\bin\windows\zookeeper-server-start.bat .\config\zookeeper.properties

# Kafka command - 
    .\bin\windows\kafka-server-start.bat .\config\server.properties

# Create Topic command -
    .\bin\windows\kafka-topics.bat --create --topic topic_name --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1

# List Topics -
    .\bin\windows\kafka-topics.bat --list --bootstrap-server localhost:9092

# To check the config of topic and partitions
    .\bin\windows\kafka-topics.bat --bootstrap-server localhost:9092 --describe --topic topic_name

# To verify that the data was successfully sent to the topic.    
    kafka-console-consumer.sh --topic etl_topic --from-beginning --bootstrap-server localhost:9092

# To run consumer file
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.2 spark_consumer.py

# Run the following command to inspect the data in Kafka:
    kafka-console-consumer --bootstrap-server localhost:9092 --topic crypto_topic --from-beginning