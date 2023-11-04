from pydantic import BaseModel

class Path(BaseModel):
    title: str
    description: str

class ActionModel(BaseModel):
    title: str
    description: str
    action: str
    age: int
    path_type: Path
    delta_in_retirement_savings: int
