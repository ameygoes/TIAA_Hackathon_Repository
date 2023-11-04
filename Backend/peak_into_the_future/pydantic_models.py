from pydantic import BaseModel


class ActionModel(BaseModel):
    title: str
    description: str
    action: str
    age: int
