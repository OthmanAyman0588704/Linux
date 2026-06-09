```python
import requests

# URL der API für die Live Uhrzeiten in New York, Berlin und Tokio
url = "http://worldtimeapi.org/api/jsonp"

# Make a GET request to the API
response = requests.get(url)

# Extract the JSON response from the response text
data = response.json()

# Print the live uhrzeiten for each city
print("New York:", data['current']['date'] + " " + data['current']['time'])
print("Berlin:", data['current']['date'] + " " + data['current']['time'])
print("Tokio:", data['current']['date'] + " " + data['current']['time'])
```
