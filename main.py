from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

@app.get('/')
def index():
    return 'manjkn'

@app.get('/about')
def about():
    return {'data' : {"about this page"}}