# config.py

# Kafka Configuration
KAFKA_TOPIC = 'etl_topic'
KAFKA_BOOTSTRAP_SERVERS = '127.0.0.1:9092'

# API Configuration
COINGECKO_BASE_URL = 'https://api.coingecko.com/api/v3'
COINGECKO_MARKETS_ENDPOINT = '/coins/markets'
COINGECKO_COIN_ENDPOINT = '/coins'
COINGECKO_API_PARAMS = {
    'vs_currency': 'usd',
    'ids': 'bitcoin,ethereum'
}

# Producer configuration
PRODUCER_INTERVAL = 2  # Time in seconds between data fetches