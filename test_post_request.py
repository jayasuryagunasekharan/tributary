import requests as requests

url = "http://0.0.0.0:8000/record"
data = {
    "engine_temperature": 0.3,
}

response = requests.post(url=url, json=data)

print(response.status_code)
print(response.content)