from pydantic import BaseModel
from tortoise.contrib.pydantic import PydanticModel   # тоже самое

class CreateUser(PydanticModel):
    username: str
    firstname: str
    lastname: str
    age: int

class UpdateUser(PydanticModel):
    firstname: str
    lastname: str
    age: int

class CreateTask(PydanticModel):
    title: str
    content: str
    priority:int

class UpdateTask (CreateTask):
    pass