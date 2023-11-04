# create a router in fastapi

from fastapi import APIRouter

router = APIRouter()

@router.get("/future/curr_profession")
def get_curr_profession():  # TODO (rohan): add dependency on JWT token
    '''
    - Will query User table and get the current profession of the user
    - will be a private method
    - will get user based on the JWT token
    '''
    return {"curr_profession": "Bachelor's student in Environmental Science"}