import requests

end_point = "http://localhost:8000/api/product/4/"

response = requests.get(end_point)

print(response.json())