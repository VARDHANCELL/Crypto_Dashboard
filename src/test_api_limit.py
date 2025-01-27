import requests

response = requests.get("https://api.coingecko.com/api/v3/your_endpoint")
print(response.headers)

# Check for rate-limiting information
rate_limit_remaining = response.headers.get('X-RateLimit-Remaining')
rate_limit_limit = response.headers.get('X-RateLimit-Limit')

print(f"Remaining API hits: {rate_limit_remaining}")
print(f"Total API hits allowed: {rate_limit_limit}")
