import requests

# Define the URL and the data
url = "http://localhost:8000/record"
data = {"engine_temperature": 0.3}

# Send the POST request
response = requests.post(url, json=data)

# Print the response
print(response.status_code)
print(response.json())
