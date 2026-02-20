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
    print(f"Update response status: {update_task_response.status_code}")
    print(f"Update response body: {update_task_response.text}")
    assert update_task_response.status_code == 200

    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    
    get_task_data = get_task_response.json()
    print(f"Get task response: {get_task_data}")
    print(f"Get task response type: {type(get_task_data)}")
    
    # Adjust assertions based on actual response structure
    assert get_task_data["content"] == updated_payload["content"]
    assert get_task_data["is_done"] == updated_payload["is_done"]


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
    return {
        "content": "Test Api Task",
        "user_id": "test_user",
        "is_done": False
    }