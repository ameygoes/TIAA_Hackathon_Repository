import pytest
from starlette.testclient import TestClient
from Backend.DBOrm import app

client = TestClient(app)

# Sample data for testing
sample_learning_data = {
    "link": "https://example.com/learning",
    "content_type": True,
    "content": "This is some learning content.",
}

def test_create_learning():
    response = client.post("/learnings/", json=sample_learning_data)
    assert response.status_code == 200
    assert response.json() == sample_learning_data

def test_get_learning():
    # Create a learning record for testing
    response = client.post("/learnings/", json=sample_learning_data)
    assert response.status_code == 200
    learning_id = response.json()["id"]

    # Retrieve the created learning record
    response = client.get(f"/learnings/{learning_id}")
    assert response.status_code == 200
    assert response.json() == sample_learning_data

def test_update_learning():
    # Create a learning record for testing
    response = client.post("/learnings/", json=sample_learning_data)
    assert response.status_code == 200
    learning_id = response.json()["id"]

    # Update the learning record
    updated_data = {
        "link": "https://new-example.com/updated",
        "content_type": False,
        "content": "Updated learning content.",
    }
    response = client.put(f"/learnings/{learning_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json() == updated_data

def test_delete_learning():
    # Create a learning record for testing
    response = client.post("/learnings/", json=sample_learning_data)
    assert response.status_code == 200
    learning_id = response.json()["id"]

    # Delete the learning record
    response = client.delete(f"/learnings/{learning_id}")
    assert response.status_code == 200
    assert response.json() == sample_learning_data  # Ensure the deleted record is returned

    # Attempt to retrieve the deleted record (should return 404)
    response = client.get(f"/learnings/{learning_id}")
    assert response.status_code == 404

if __name__ == "__main__":
    pytest.main()
