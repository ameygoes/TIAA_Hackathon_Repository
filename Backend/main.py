# create a starter fastapi app
# run with uvicorn main:app --reload

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from playhouse.shortcuts import model_to_dict
import peewee
from DBOrm import User, db
from passlib.context import CryptContext
from auth_handler import signJWT
from typing import Optional

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a Pydantic model for the JWT token
class Token(BaseModel):
    access_token: str
    token_type: str

# JWT settings
SECRET_KEY = "your-secret-key"  # Replace with a secure secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Adjust as needed

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    name: Optional[str] = 'name'
    karma_points: Optional[int] = 0
    retirement_age: Optional[int] = 0
    retirement_amt_per_year: Optional[int] = 0
    birth_year: Optional[int] = 0
    current_saved_money: Optional[int] = 0
    current_profession: Optional[str] = ''
    current_education: Optional[str] = ''
    debt_in_K: Optional[int] = 0
    workex: Optional[bool] = 0
    monthly_burn_rate: Optional[int] = 0
    transactionId: Optional[int] = 0
    username: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str

class UserLogin(BaseModel):
    username: str
    password: str


@app.post("/register", status_code=200)
async def register_user(user:UserCreate):
    try:
        db_user = db.execute(User.select().where(User.username == user.username)).fetchone()
        if db_user is not None:
            raise Exception
        User.create(**user.dict())
        return signJWT(user.username)
    except Exception:
        raise HTTPException(status_code=400, detail="Username already registered")

@app.post("/login")
def login_user(user: UserLogin):
    db_user = User.get(User.username == user.username)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    # Create a JWT token
    return signJWT(user.username)

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)