import requests
ENDPOINT = "http://todo.pixegami.io"

response = requests.get(ENDPOINT)
status_code = response.status_code
print(response.json())
print(status_code)

def test_get_todo():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    pass


test_get_todo()