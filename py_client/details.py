import requests
from login import authLogin

end_point = "http://localhost:8000/api/product/7/"
token = authLogin()
if token is not None:
    response = requests.get(end_point, headers={"Authorization": f"Bearer {token}"})
    print(response.json())
else:
    raise Exception("invalid credentials")
