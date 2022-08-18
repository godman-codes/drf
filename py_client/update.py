import requests

end_point = "http://localhost:8000/api/product/1/update"


response = requests.put(end_point, json={'title': 'samrt', 'content': 'hello world', 'price': 66.3})


print(response.json())