import requests

response = requests.get("https://api.coingecko.com/api/v3/your_endpoint")
print(response.headers)
