import os
from dotenv import load_dotenv

load_dotenv()  # Loads .env file variables into environment

DATABASE_URL = os.getenv("DATABASE_URL")

from databases import Database
from sqlalchemy import MetaData, create_engine

database = Database(DATABASE_URL)
metadata = MetaData()
engine = create_engine(DATABASE_URL)
