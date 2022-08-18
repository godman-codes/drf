import requests

end_point = "http://localhost:8000/api/product/" # this is the same endpoint as the one for the create view

response = requests.get(end_point)
print(response.json())