from kafka import KafkaProducer # pre defined class to send data to kafka topics
from data_fetcher import fetch_data_and_send_to_kafka  # used to work with json data
import config
import time

# import logging
# logging.basicConfig(level=logging.DEBUG)



def main():
    # an object (of the kafkaproducer class) will be used to send data to kafka topic 
    producer = KafkaProducer(
        
        # bootstrap_servers stores the kafka broker address
        bootstrap_servers = config.KAFKA_BOOTSTRAP_SERVERS,
        
        # here converting into jsondumps and then into bytes
        value_serializer = lambda v: str(v).encode('utf-8'))
        # key_serializer=lambda k: k.encode('utf-8') )
    
    while True:
        # Fetch data from CoinGecko and send it to Kafka
        fetch_data_and_send_to_kafka(producer)
        
        # flush is a method called in respect of producer object
        # responsible for releasing all the batches regardless of any scenario and returns only when the broker acknowledges of the data
        # Synchronous process
        producer.flush()
        print("All messages have been sent to Kafka.")
        
         # Sleep for a specified interval before sending the next batch of data
        time.sleep(config.PRODUCER_INTERVAL)

# Main logic
# runs only if the script is executed directly (not if it's imported as a module in another script).
if __name__ == "__main__":
    main()