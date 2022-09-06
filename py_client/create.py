import requests

end_point = "http://localhost:8000/api/products/"

# response = requests.get(end_point, json={'query': 'hello world'})
response = requests.post(end_point, json={'title': 'smart', 'price': 66.3})

print(response.json())