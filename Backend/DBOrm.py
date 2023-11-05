from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List 
from peewee import Model, SqliteDatabase, CharField, IntegerField, BooleanField, fn, ForeignKeyField
import random
import names
from faker import Faker

# Define a SQLite database connection
db = SqliteDatabase('tiaa.db')

class BaseModel_for_Tables(Model):
    class Meta:
        database = db

class Transaction(BaseModel_for_Tables):
    userId = IntegerField()
    transactionCategory = CharField(max_length=255)
    transactionAmount = IntegerField()

class User(BaseModel_for_Tables):
    name = CharField(max_length=255)
    karma_points = IntegerField()
    retirement_age = IntegerField()
    retirement_amt_per_year = IntegerField()
    birth_year = IntegerField()
    current_saved_money = IntegerField()
    current_profession = CharField(max_length=255)
    current_education = CharField(max_length=255)
    debt_in_K = IntegerField()
    workex = BooleanField()
    monthly_burn_rate = IntegerField()
    transactionId = IntegerField()
    username = CharField(max_length=25)
    password = CharField(max_length=25)


class Learning(BaseModel_for_Tables):
    link = CharField(max_length=500)
    content_type = BooleanField()
    content = CharField(max_length=10000)

class Friendship(BaseModel_for_Tables):
    user1  = ForeignKeyField(User, backref='friends')
    user2 = ForeignKeyField(User, backref='others_friend')
    
# Create FastAPI app
app = FastAPI()


# =========================================================================
# ============================ USER CRUD ==================================
# =========================================================================
# Pydantic model for creating User records
class CreateUser(BaseModel):
    name: str
    karma_points: int
    retirement_age: int
    retirement_amt_per_year: int
    birth_year: int
    current_saved_money: int
    current_profession: str
    current_education: str
    debt_in_K: int
    workex: bool
    monthly_burn_rate: int
    transactionId: int
    username: str
    password: str


@app.post("/users/", response_model=CreateUser)
async def create_user(user_data: CreateUser):
    db.connect()
    try:
        # Create a new User record with the data
        user = User.create(
                name=user_data.name,
                karma_points=user_data.karma_points,
                retirement_age=user_data.retirement_age,
                retirement_amt_per_year=user_data.retirement_amt_per_year,
                birth_year=user_data.birth_year,
                current_saved_money=user_data.current_saved_money,
                current_profession=user_data.current_profession,
                current_education=user_data.current_education,
                debt_in_K=user_data.debt_in_K,
                workex=user_data.workex,
                monthly_burn_rate=user_data.monthly_burn_rate,
                transactionId=user_data.transactionId,
                username=user_data.username,
                password=user_data.password
            )
        db.commit()
        return user
    except Exception as e:

        db.rollback()
        raise e
    finally:
        db.close()

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    try:
        with db:
            user = User.get(User.id == user_id)
            print(user)
            print(type(user))
            return { "name":user.name,
                "karma_points":user.karma_points,
                "retirement_age":user.retirement_age,
                "retirement_amt_per_year":user.retirement_amt_per_year,
                "birth_year":user.birth_year,
                "current_saved_money":user.current_saved_money,
                "current_profession":user.current_profession,
                "current_education":user.current_education,
                "debt_in_K":user.debt_in_K,
                "workex":user.workex,
                "monthly_burn_rate":user.monthly_burn_rate,
                "transactionId":user.transactionId,
                "username":user.username,
                "password":user.password}
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}")
async def update_user(user_id: int, user_data: CreateUser):
    try:
        with db:
            user = User.get(User.id == user_id)
            user.name = user_data.name
            user.karma_points = user_data.karma_points
            user.retirement_age = user_data.retirement_age
            user.retirement_amt_per_year = user_data.retirement_amt_per_year
            user.birth_year = user_data.birth_year
            user.current_saved_money = user_data.current_saved_money
            user.current_profession = user_data.current_profession
            user.current_education = user_data.current_education
            user.debt_in_K = user_data.debt_in_K
            user.workex = user_data.workex
            user.monthly_burn_rate = user_data.monthly_burn_rate
            user.transactionId = user_data.transactionId
            user.save()
            return user
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}", response_model=dict)
async def delete_user(user_id: int):
    try:
        with db:
            user = User.get(User.id == user_id)
            user.delete_instance()
            return {"message": "User deleted successfully"}
    except User.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")


# =========================================================================
# ============================ TRANSACTIONS CRUD ==========================
# =========================================================================

# Pydantic model for creating Transaction records
class CreateTransaction(BaseModel):
    userId: int
    transactionCategory: str
    transactionAmount: int

# Endpoint to create a Transaction record
@app.post("/transactions/", response_model=CreateTransaction)
async def create_transaction(transaction: CreateTransaction):
    db.connect()
    try:
        transaction = Transaction.create(
            userId=transaction.userId,
            transactionCategory=transaction.transactionCategory,
            transactionAmount=transaction.transactionAmount,
        )
        db.commit()
        return transaction
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Endpoint to retrieve a Transaction record by ID
@app.get("/transactions/{transaction_id}", response_model=CreateTransaction)
async def get_transaction(transaction_id: int):
    db.connect()
    try:
        transaction = Transaction.get(Transaction.id == transaction_id)
        return transaction
    except Transaction.DoesNotExist:
        raise HTTPException(status_code=404, detail="Transaction not found")
    finally:
        db.close()

# Endpoint to update a Transaction record by ID
@app.put("/transactions/{transaction_id}", response_model=CreateTransaction)
async def update_transaction(transaction_id: int, updated_data: CreateTransaction):
    db.connect()
    try:
        transaction = Transaction.get(Transaction.id == transaction_id)
        transaction.transactionCategory = updated_data.transactionCategory
        transaction.transactionAmount = updated_data.transactionAmount
        transaction.save()
        return transaction
    except Transaction.DoesNotExist:
        raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Endpoint to delete a Transaction record by ID
@app.delete("/transactions/{transaction_id}", response_model=CreateTransaction)
async def delete_transaction(transaction_id: int):
    db.connect()
    try:
        transaction = Transaction.get(Transaction.id == transaction_id)
        transaction.delete_instance()
        db.commit()
        return transaction
    except Transaction.DoesNotExist:
        raise HTTPException(status_code=404, detail="Transaction not found")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Endpoint to get all transactions of a User grouped by categories and summed over counts
@app.get("/transactions/grouped/{user_id}", response_model=Dict[str, int])
async def get_transactions_grouped(user_id: int):
    db.connect()
    try:
        # Query to group transactions by category and sum over counts
        result = (
            Transaction
            .select(Transaction.transactionCategory, fn.Sum(Transaction.transactionAmount).alias('SumOfAmountInCategory'))
            .where(Transaction.userId == user_id)
            .group_by(Transaction.transactionCategory)
        )

        # Convert the result to a dictionary
        grouped_transactions = {row.transactionCategory: row.SumOfAmountInCategory for row in result}

        return grouped_transactions
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        db.close()


# =========================================================================
# ============================ LEARNINGS CRUD =============================
# =========================================================================

# Pydantic model for creating Learning records
class CreateLearning(BaseModel):
    link: str
    content_type: bool #True means its a Video False means its a text content
    content: str

# Endpoint to create a Learning record
@app.post("/learnings/", response_model=CreateLearning)
async def create_learning(learning: CreateLearning):
    db.connect()
    try:
        learning = Learning.create(
            link=learning.link,
            content_type=learning.content_type,
            content=learning.content,
        )
        db.commit()
        return learning
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# Endpoint to retrieve a Learning record by ID
@app.get("/learnings/{learning_id}", response_model=CreateLearning)
async def get_learning(learning_id: int):
    db.connect()
    try:
        learning = Learning.get(Learning.id == learning_id)
        return learning
    except Learning.DoesNotExist:
        raise HTTPException(status_code=404, detail="Learning record not found")
    finally:
        db.close()

# Endpoint to update a Learning record by ID
@app.put("/learnings/{learning_id}", response_model=CreateLearning)
async def update_learning(learning_id: int, updated_data: CreateLearning):
    db.connect()
    try:
        learning = Learning.get(Learning.id == learning_id)
        learning.link = updated_data.link
        learning.content_type = updated_data.content_type
        learning.content = updated_data.content
        learning.save()
        return learning
    except Learning.DoesNotExist:
        raise HTTPException(status_code=404, detail="Learning record not found")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Endpoint to delete a Learning record by ID
@app.delete("/learnings/{learning_id}", response_model=CreateLearning)
async def delete_learning(learning_id: int):
    db.connect()
    try:
        learning = Learning.get(Learning.id == learning_id)
        learning.delete_instance()
        db.commit()
        return learning
    except Learning.DoesNotExist:
        raise HTTPException(status_code=404, detail="Learning record not found")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# =========================================================================
# ============================ FRIENDSHIPS CRUD =============================
# =========================================================================

# Pydantic model for creating Learning records
class CreateFriendship(BaseModel):
    user1: int
    user2: int 

@app.get("/users/{user_id}/friends", response_model=List[CreateUser])
async def get_friends(user_id: int):
    db.connect()
    try:
        # Find all friendships where the user is either user1 or user2
        friendships = Friendship.select().where((Friendship.user1 == user_id) | (Friendship.user2 == user_id))
        
        friend_ids = []
        for friendship in friendships:
            if friendship.user1 == user_id:
                friend_ids.append(friendship.user2)
            else:
                friend_ids.append(friendship.user1)
        
        # Retrieve user data for the friend_ids
        friends = User.select().where(User.id << friend_ids)
        
        return list(friends)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to fetch friends")
    finally:
        db.close()

# Endpoint to create a Friendship record
@app.post("/friendships/", response_model=CreateFriendship)
async def create_friendship(friendship_data: CreateFriendship):
    db.connect()
    try:
        friendship = Friendship.create(
            user1=friendship_data.user1,
            user2=friendship_data.user2
        )
        db.commit()
        return friendship
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Endpoint to retrieve a Friendship record by ID
@app.get("/friendships/{friendship_id}", response_model=CreateFriendship)
async def get_friendship(friendship_id: int):
    db.connect()
    try:
        friendship = Friendship.get(Friendship.id == friendship_id)
        return friendship
    except Friendship.DoesNotExist:
        raise HTTPException(status_code=404, detail="Friendship record not found")
    finally:
        db.close()

# Endpoint to update a Friendship record by ID
@app.put("/friendships/{friendship_id}", response_model=CreateFriendship)
async def update_friendship(friendship_id: int, updated_data: CreateFriendship):
    db.connect()
    try:
        friendship = Friendship.get(Friendship.id == friendship_id)
        friendship.user1 = updated_data.user1
        friendship.user2 = updated_data.user2
        friendship.save()
        return friendship
    except Friendship.DoesNotExist:
        raise HTTPException(status_code=404, detail="Friendship record not found")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# Endpoint to delete a Friendship record by ID
@app.delete("/friendships/{friendship_id}", response_model=CreateFriendship)
async def delete_friendship(friendship_id: int):
    db.connect()
    try:
        friendship = Friendship.get(Friendship.id == friendship_id)
        friendship.delete_instance()
        db.commit()
        return friendship
    except Friendship.DoesNotExist:
        raise HTTPException(status_code=404, detail="Friendship record not found")
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

# =========================================================================
# ======================== INSERT FAKE DATA : USER ========================
# =========================================================================

# Function to generate random user data
def generate_random_user():
    fake = Faker()
    user_data = {
        "name": names.get_full_name(),
        "karma_points": random.randint(0, 100),
        "retirement_age": random.randint(60, 70),
        "retirement_amt_per_year": random.randint(10000, 30000),
        "birth_year": random.randint(1950, 2000),
        "current_saved_money": random.randint(10000, 50000),
        "current_profession": fake.job(),
        "current_education": fake.random_element(elements=("High School", "Bachelor's Degree", "Master's Degree", "Ph.D.")),
        "debt_in_K": random.randint(0, 50),
        "workex": random.choice([True, False]),
        "monthly_burn_rate": random.randint(1000, 5000),
        "transactionId": random.randint(1, 100),
        "username": f"username_{random.randint(0, 1000000)}",
        "password": "password"
    }
    return user_data

# Function to generate random user data
def generate_transactions():
    return {
        "userId": random.randint(1, 100),
        "transactionCategory": random.choice(["Expense", "Income", "Groceries", "Entertainment", "Healthcare", "Transportation"]),
        "transactionAmount": round(random.uniform(1.0, 1000.0), 2),
        }


# Function to generate random user data
def generate_learnings():
    fake = Faker()
    learning_data = {
        "link": fake.url(),
        "content_type": random.choice(["True", "False"]),
        "content": fake.text(),
    }
    return learning_data

# Function to generate random user data
def generate_friendships():
    friendship_data = {
        "user1": random.randint(1,20),
        "user2": random.randint(1,20)
    }
    return friendship_data


# Endpoint to insert a random user
@app.post("/insert_random_user/{number_of_users}", response_model=str)
async def insert_random_user(number_of_users: int):
    db.connect()

    for _ in range(number_of_users):
        user_data = generate_random_user()
        try:
            user = User.create(**user_data)
            db.commit()
            continue
        
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            db.close()
    return f"{number_of_users} users Added Succesfully."

# Endpoint to insert a random user
@app.post("/insert_random_transaction/{number_of_transactions}", response_model=str)
async def insert_random_transaction(number_of_transactions: int):
    db.connect()

    for _ in range(number_of_transactions):
        transaction_data = generate_transactions()
        try:
            user = Transaction.create(**transaction_data)
            db.commit()
            continue
        
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            db.close()
    return f"{number_of_transactions} transactions Added Succesfully."


# Endpoint to insert a random user
@app.post("/insert_random_learning/{number_of_learnings}", response_model=str)
async def insert_random_learning(number_of_learnings: int):
    db.connect()

    for _ in range(number_of_learnings):
        learning_data = generate_learnings()
        try:
            user = Learning.create(**learning_data)
            db.commit()
            continue
        
        except Exception as e:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            db.close()
    return f"{number_of_learnings} learnings Added Succesfully."


# Endpoint to insert a random user
@app.post("/insert_random_friendships/{number_of_friendships}", response_model=str)
async def insert_random_friendships(number_of_friendships: int):
    db.connect()

    for _ in range(number_of_friendships):
        friendship_data = generate_friendships()
        try:
            user = Friendship.create(**friendship_data)
            db.commit()
            continue
        
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        finally:
            db.close()
    return f"{number_of_friendships} friendships Added Succesfully."

def createTables():
    print("Creating Tables...")
    with db:
        db.create_tables([User, Transaction, Learning, Friendship], safe=True)
    print("Tables Created!!!")

if __name__ == '__main__':
    createTables()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
