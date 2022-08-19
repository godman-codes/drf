import requests

end_point = "http://localhost:8000/api/product/1/update/"

data =  {
    'title': 'tobit update',
    'price': 666.3
    }
response = requests.put(end_point, json=data)


print(response.json())