import requests
import uuid

# login
print('\ntest login token')
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

# query task
print('\ntest task query')
resp = requests.get(
    url='http://localhost:8000/api/task/?id=1',
    headers={"Authentication": token}
)
print(resp)
print(resp.status_code)
print(resp.content)
print(resp.json())

# create/update task
print('\ntest task create/update')
resp = requests.post(
    url='http://localhost:8000/api/task/',
    headers={"Authentication": token},
    data={'title': 'test', 'group_id': uuid.uuid1()}
    # data={'id':2, 'title': 'test', 'group_id': 'uuid'}
)
print(resp)
print(resp.status_code)
print(resp.content)
print(resp.json())

# query tasks
print('\ntest tasks query')
resp = requests.get(
    url='http://localhost:8000/api/tasks/?title=test',
    headers={"Authentication": token}
)
print(resp)
print(resp.status_code)
print(resp.content)
print(resp.json())
