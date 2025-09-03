# schemas.py
from pydantic import BaseModel

class BlogCreate(BaseModel):
    title: str
    content: str

class BlogOut(BlogCreate):
    id: int  # include ID for responses

class User(BaseModel):
    id: int
    name : str
