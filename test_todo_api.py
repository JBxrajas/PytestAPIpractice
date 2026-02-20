import requests
from uuid import uuid4
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

    task_id = data["task"]["task_id"]  # Changed from data["task"][task_id]
    create_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    assert create_task_response.status_code == 200
    get_task_data = create_task_response.json()

    assert get_task_data["content"] == payload["content"]  
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_task():
    # First, create a task to update
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    
    # update task - Include task_id in payload
    updated_payload = {
        "task_id": task_id,  # Must include task_id
        "content": "Updated Test Api Task",
        "user_id": payload["user_id"],
        "is_done": True
    }

    update_task_response = update_task(updated_payload)
    assert update_task_response.status_code == 200

    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    
    get_task_data = get_task_response.json()
    
    # Adjust assertions based on actual response structure
    assert get_task_data["content"] == updated_payload["content"]
    assert get_task_data["is_done"] == updated_payload["is_done"]

def test_can_list_tasks():
    n = 3
    payload = new_task_payload()  # Create payload once to get consistent user_id
    user_id = payload["user_id"]  # Store the user_id
    
    for i in range(n):
        task_payload = new_task_payload()
        task_payload["user_id"] = user_id  # Use same user_id for all tasks
        create_task_response = create_task(task_payload)
        assert create_task_response.status_code == 200
    
    list_response = list_tasks(user_id)
    data = list_response.json()
    tasks = data["tasks"]
    assert len(tasks) == n  # Ensure exactly n tasks are returned
    

def test_can_delete_task():
    # Create a task to delete
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]
    
    # Delete the task
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200
    
    # Verify task is deleted - should get 404 or empty response
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")

def new_task_payload():
    user_id = "test_user_" + uuid4().hex # Generate unique user_id
    return {
        "content": "Test Api Task",
        "user_id": user_id,  
        "is_done": False
    }
def list_tasks(user_id):
    return requests.get(ENDPOINT + "/list-tasks/"+user_id)