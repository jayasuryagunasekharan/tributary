import requests

# Define the URLs
record_url = "http://localhost:8000/record"
collect_url = "http://localhost:8000/collect"

# Test the record endpoint
record_data = {"engine_temperature": 5}
response = requests.post(record_url, json=record_data)
print("Record Response:", response.json())

# Test the collect endpoint
response = requests.post(collect_url)
print("Collect Response:", response.json())
