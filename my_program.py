import requests

url = "http://127.0.0.1:8000/api/v1/articles/json-drf/"
response = requests.get(url)

print(response.json)
