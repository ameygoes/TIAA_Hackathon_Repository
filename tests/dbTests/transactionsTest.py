import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Replace these values with your test data
test_user_id = 1
test_transaction_data = {
    "userId": 1,
    "transactionCategory": "Groceries",
    "transactionAmount": 50
}

def test_create_transaction():
    response = client.post("/transactions/", json=test_transaction_data)
    assert response.status_code == 200
    assert response.json()["userId"] == test_user_id
    assert response.json()["transactionCategory"] == test_transaction_data["transactionCategory"]
    assert response.json()["transactionAmount"] == test_transaction_data["transactionAmount"]

def test_get_transaction_by_id():
    # First, create a test transaction
    response = client.post("/transactions/", json=test_transaction_data)
    transaction_id = response.json()["id"]

    # Now, retrieve the transaction by ID
    response = client.get(f"/transactions/{transaction_id}")
    assert response.status_code == 200
    assert response.json()["id"] == transaction_id

def test_update_transaction():
    # First, create a test transaction
    response = client.post("/transactions/", json=test_transaction_data)
    transaction_id = response.json()["id"]

    # Update the transaction
    updated_data = {"transactionCategory": "Clothing", "transactionAmount": 75}
    response = client.put(f"/transactions/{transaction_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["transactionCategory"] == updated_data["transactionCategory"]
    assert response.json()["transactionAmount"] == updated_data["transactionAmount"]

def test_delete_transaction():
    # First, create a test transaction
    response = client.post("/transactions/", json=test_transaction_data)
    transaction_id = response.json()["id"]

    # Delete the transaction
    response = client.delete(f"/transactions/{transaction_id}")
    assert response.status_code == 200

def test_get_transactions_grouped():
    response = client.get(f"/transactions/grouped/{test_user_id}")
    assert response.status_code == 200
    grouped_transactions = response.json()
    # Add assertions to check the grouped transaction data
    # For example: assert "Groceries" in grouped_transactions
    # and assert grouped_transactions["Groceries"] == total_amount
