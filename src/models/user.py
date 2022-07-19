from enum import Enum
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class Gender(Enum):
    Male = "Male"
    Female = "Female"
    Others = "Others"

class Roles(Enum):
    superuser = "superuser"
    user = "user"

class User(BaseModel):
    id: Optional[UUID]=None
    name: Optional[str]=None
    email: str
    password: str
    gender: Optional[Gender]=None
    role: Optional[Roles]=None
    age: Optional[int]=None
    profession: Optional[str]=None

class UserCreate(User):
    name: str
    email: str
    password: str
    gender: str
    age: int
    profession: str

class UserFetch(User):
    name: str
    email: str
    gender: str
    profession: str
    age: int

    class Config:
        orm_mode = True

class LoginUserBody(User):
    email: str
    password: str
