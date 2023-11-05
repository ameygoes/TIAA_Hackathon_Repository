# TIAA_Hackathon_Repository

# Setting Up the backend Server

## Step 1: Clone the Repository

Clone this project's repository to your local machine using Git and go inside the repository directory.

```shell
git clone <repository-url>
```

## Step 2: Install the requirements using pip in your virtual environment
```shell
pip install -r requirements.txt
```
## Step 3: Set up the environment file
Create a .env file and add this contents to it
algorithm=HS256
secret=deff1952d59f883ece260e8683fed21ab0ad9a53323eca4f

## Step 4: Start the server
```shell
python main.py
```

- **Register User**: Allows users to register with a unique username and password. Upon successful registration, it returns a JWT token.

- **Login User**: Allows registered users to log in using their username and password. It returns a JWT token upon successful login.

- **Leaderboard**: Displays a leaderboard of users sorted by their "karma points." It requires authentication with a JWT token.

## Endpoints

### Register User

- **POST** `/register`

  Register a new user. It expects a JSON request with a username and password. If the username is unique, a new user is created, and a JWT token is returned. If the username already exists, an error response is returned.

### Login User

- **POST** `/login`

  Log in as an existing user. It expects a JSON request with a username and password. If the credentials are correct, a JWT token is returned. If not, an error response is returned.

### Leaderboard

- **GET** `/leaderboard`

  Get the leaderboard of users sorted by "karma points." It requires authentication with a JWT token. The endpoint returns a list of friends with their usernames and karma points.

