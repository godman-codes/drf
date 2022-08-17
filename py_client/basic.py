import requests

end_point = "http://localhost:8000/api/"

# response = requests.get(end_point, json={'query': 'hello world'})
response = requests.post(end_point, json={'title': None, 'content': 'hello world', 'price': 'sf'})

print(response.json())