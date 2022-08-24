import requests
from getpass import getpass # this is to create a custom command line input receiver without displaying the content of the fields this is very good for passwords
def authLogin():
    auth_endpoint = "http://localhost:8000/api/auth/" # this is the same endpoint as the one for the create view
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    auth_response = requests.post(auth_endpoint, json={
        "username": username,
        "password": password
    })
    if auth_response.status_code == 200:
        print(auth_response.json())
        return auth_response.json().get('token')
    else:
        print('Invalid credentials')
        return None