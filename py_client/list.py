import requests
from getpass import getpass # this is to create a custom command line input receiver without displaying the content of the fields this is very good for passwords
from login import authLogin

token = authLogin()
if token is not None:
    print('smart')
    end_point = "http://localhost:8000/api/product/" # this is the same endpoint as the one for the create view
    response = requests.get(end_point, headers={"Authorization": f"Token {token}"})
    print(response.json())
else:
    raise Exception('invalid credentials')