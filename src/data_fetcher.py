# import requests # used for making HTTP requests to fetch data from APIs.
# import json # used to convert Python objects to JSON format and vice versa.
# import config # contains configuration values

# def fetch_coin_data():
    
#     # Base URL from config
#     base_url = config.COINGECKO_BASE_URL
    
#     # Fetch market data for Bitcoin and Ethereum using the configured endpoint and params
#     markets_url = f"{base_url}{config.COINGECKO_MARKETS_ENDPOINT}"
#     response = requests.get(markets_url, params=config.COINGECKO_API_PARAMS)
#     markets_data = response.json()
    
#     # Fetch details about Bitcoin using the configured endpoint
#     bitcoin_url = f"{base_url}{config.COINGECKO_COIN_ENDPOINT}/bitcoin"
#     response = requests.get(bitcoin_url)
#     bitcoin_data = response.json()
    
#     return {
#         'markets_data': markets_data,
#         'bitcoin_data': bitcoin_data
#     }

# def fetch_data_and_send_to_kafka(producer):
#     data = fetch_coin_data()
    
#     # Send data to Kafka using the topic from the config file
#     producer.send(config.KAFKA_TOPIC, key=b'market_data', value=json.dumps(data['markets_data']).encode('utf-8'))
#     producer.send(config.KAFKA_TOPIC, key=b'bitcoin_data', value=json.dumps(data['bitcoin_data']).encode('utf-8'))

#     print(f"Data sent to Kafka topic '{config.KAFKA_TOPIC}'")

import requests
import json
import config  # contains configuration values

def fetch_coin_data():
    # Base URL from config
    base_url = config.COINGECKO_BASE_URL
    
    # Fetch the top 100 cryptocurrencies by market cap
    markets_url = f"{base_url}{config.COINGECKO_MARKETS_ENDPOINT}"
    response = requests.get(markets_url, params={**config.COINGECKO_API_PARAMS, "per_page": 100, "page": 1})
    if response.status_code != 200:
        raise Exception(f"Error fetching data from API: {response.status_code} - {response.text}")
    markets_data = response.json()
    return markets_data

def fetch_data_and_send_to_kafka(producer):
    try:
        # Fetch coin data
        data = fetch_coin_data()

        # Send data to Kafka
        producer.send(config.KAFKA_TOPIC, key=b'market_data', value=json.dumps(data).encode('utf-8'))
        print(f"Data sent to Kafka topic '{config.KAFKA_TOPIC}'")
    except Exception as e:
        print(f"Error in fetch_data_and_send_to_kafka: {e}")
