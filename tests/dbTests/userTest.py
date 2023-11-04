import requests

# Define the URL of your FastAPI application
base_url = "http://localhost:8000"  # Adjust the URL as needed

# Define the endpoint for creating a User record
endpoint = "/users/"

# Define the data for creating a new user
user_data = {
    "name": "John Doe",
    "karma_points": 100,
    "retirement_age": 65,
    "retirement_amt_per_year": 20000,
    "birth_year": 1980,
    "current_saved_money": 50000,
    "current_profession": "Engineer",
    "current_education": "Bachelor's Degree",
    "debt_in_K": 10000,
    "workex": True,
    "monthly_burn_rate": 1500,
    "transactionId": 1  # Replace with the actual transaction ID
}

# Send a POST request to create the user
response = requests.post(f"{base_url}{endpoint}", json=user_data)

if response.status_code == 201:
    print("User created successfully!")
    user = response.json()
    print(f"User ID: {user['id']}")
else:
    print(f"Failed to create the user. Status code: {response.status_code}")
