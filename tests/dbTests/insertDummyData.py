# Import necessary modules and classes
from fastapi import FastAPI
from pydantic import BaseModel
from peewee import SqliteDatabase, Model, CharField, IntegerField, BooleanField
import random
import names
from faker import Faker

# Create a FastAPI app
app = FastAPI()

# Define your Peewee models and database connection
DB_NAME = "your_database_name.db"
db = SqliteDatabase(DB_NAME)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
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



if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
