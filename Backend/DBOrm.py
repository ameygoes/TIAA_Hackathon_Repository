from fastapi import FastAPI
from peewee import Model, SqliteDatabase, CharField, IntegerField, BooleanField, ForeignKeyField
from dbconfig import *

# Define a SQLite database connection
db = SqliteDatabase(DB_NAME)

class BaseModel(Model):
    class Meta:
        database = db

class Transaction(BaseModel):
    userId = IntegerField()
    transactionCategory = CharField(max_length=255)
    transactionAmount = IntegerField()

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
    username = CharField(max_length=25)
    password = CharField(max_length=25)
    
    class Meta:
        database = db

class Learning(BaseModel):
    link = CharField(max_length=500)
    content_type = BooleanField()
    content = CharField(max_length=10000)

class Friendship(BaseModel):
    user1  = ForeignKeyField(User, backref='friends')
    user2 = ForeignKeyField(User, backref='others_friend')

def insert_record(table_class, **kwargs):
    db.connect()
    try:
        record = table_class.create(**kwargs)
        db.commit()
        return record
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# # Insert a User record
# user = insert_record(User, name="John Doe", karma_points=100)
# print(f"User ID: {user.id}")

# # Insert a Transaction record
# transaction = insert_record(Transaction, userId=user.id, transactionCategory="Purchase", transactionAmount=50)
# print(f"Transaction ID: {transaction.id}")

# # Insert a Learning record
# learning = insert_record(Learning, link="example.com", content_type=True, content="This is a learning record.")
# print(f"Learning ID: {learning.id}")

def create_tables():
    db.connect()
    db.create_tables([Transaction, User, Learning, Friendship])
    db.close()

if __name__ == '__main__':

    create_tables()