import requests

product_id = input('What is the product id? ') # input the product id

try: # try to convert the input to an integer
    product_id = int(product_id)
except: # if it fails, print an error message
    print(f'"{product_id}" is not a valid product id')

if product_id: 
    end_point = f"http://localhost:8000/api/product/{product_id}/delete/"
    response = requests.delete(end_point)
    print(response.status_code == 204) # True if the status code is 204