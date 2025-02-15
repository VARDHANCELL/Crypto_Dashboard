# config.py

# Kafka Configuration
KAFKA_TOPIC = 'etl_topic'
KAFKA_BOOTSTRAP_SERVERS = '127.0.0.1:9092'

# API Configuration
COINGECKO_BASE_URL = 'https://api.coingecko.com/api/v3'
COINGECKO_MARKETS_ENDPOINT = '/coins/markets'
COINGECKO_COIN_ENDPOINT = '/coins'
# COINGECKO_API_PARAMS = {
#     'vs_currency': 'usd',
#     'ids': 'bitcoin,ethereum'
# }

COINGECKO_API_PARAMS = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 100,  # Fetch top 100 coins
    "page": 1,
    "sparkline": False
}


# Producer configuration
PRODUCER_INTERVAL = 2  # Time in seconds between data fetches