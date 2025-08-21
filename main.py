from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get('/')
def index():
    return 'hii'

@app.get('/about')
def about():
    return {'data' : {"about page"}}