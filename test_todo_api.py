import requests
ENDPOINT = "http://todo.pixegami.io"

def test_get_todo():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200
    pass


def test_create_task():
    payload = new_task_payload()
    create_task_response= create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    print(data)

    task_id = data["task"]["task_id"]  # Changed from data["task"][task_id]
    create_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    assert create_task_response.status_code == 200
    get_task_data = create_task_response.json()

    assert get_task_data["content"] == payload["content"]  
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_task():
    # First, create a task to update
    #update task
    #get validate the changes
    pass

def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def new_task_payload():
    return {
        "content": "Test Api Task",
        "user_id": "test_user",
        "is_done": False
    }