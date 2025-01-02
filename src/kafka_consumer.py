from kafka import KafkaConsumer
import config

# Define the Kafka consumer
consumer = KafkaConsumer(
    config.KAFKA_TOPIC,  # Replace with your topic name
    bootstrap_servers=[config.KAFKA_BOOTSTRAP_SERVERS],  # Adjust the Kafka broker if needed
    auto_offset_reset='earliest',  # Start reading at the earliest message
    enable_auto_commit=True,  # Automatically commit offsets
    group_id='etl_group',  # Consumer group name
    value_deserializer=lambda x: x.decode('utf-8')  # Deserialize the message
)

# Start consuming messages
for message in consumer:
  print(f"Received message: {message.value}")

consumer.close()  # Close the consumer after stopping
