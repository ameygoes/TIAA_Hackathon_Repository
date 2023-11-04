# create a router in fastapi

from typing import List, Optional
from fastapi import APIRouter
from pydantic import BaseModel

from peak_into_the_future.pydantic_models import ActionModel
from prompter import ActionPrompter

router = APIRouter(
    prefix="/future",
    tags=["future"],
    responses={404: {"description": "Not found"}},
)
action_prompter = ActionPrompter()

@router.get("/curr_profession")
def get_curr_profession(user):  # TODO (rohan): add dependency on JWT token
    '''
    - Will query User table and get the current profession of the user
    - will be a private method
    - will get user based on the JWT token
    '''
    return {"curr_profession": "Bachelor's student in Environmental Science"}


class User(BaseModel):
    curr_summary: str
    retirement_goals: str

# TODO (rohan): add dependency on JWT token
@router.post("/actionable_options")
def get_actionable_options(user: User, prev_actions: Optional[List[ActionModel]]) -> List[ActionModel]:
    '''
    - Will query User table and get current profile and retirement goals of the user
    - Will send this information with the prev actions list to the prompter
    '''
    next_action_options: List[ActionModel] = action_prompter(user.curr_summary, user.retirement_goals, prev_actions)
    return next_action_options

