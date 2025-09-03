# create.py

from models import Base
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:yourpassword@localhost:5432/fastapi_db"

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)
print("✅ Tables created.")


