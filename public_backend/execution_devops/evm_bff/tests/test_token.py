import requests


resp = requests.post(
    url='http://localhost:8000/api/login/',
    data={
        "username": "test",
        "password": "test",
    }
)
print(resp)
print(resp.status_code)
print(resp.content)
token = resp.json()['data']['token']

resp = requests.get(
    url='http://localhost:8000/api/tasks/',
    headers={"Authentication": token}
)
print(resp)
print(resp.status_code)
print(resp.content)
# print(resp.json())
