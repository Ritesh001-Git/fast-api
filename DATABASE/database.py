from fastapi import FastAPI
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

load_dotenv()

MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT")

# DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
DATABASE_URL = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}"
    f"@localhost/{MYSQL_DB}"
    f"?unix_socket=/tmp/mysql.sock"
)

print("HOST:", MYSQL_HOST)
print("USER:", MYSQL_USER)
print("DB:", MYSQL_DB)
print("PORT:", MYSQL_PORT)
print(DATABASE_URL)

# Connection 
engine = create_engine(DATABASE_URL)

# Session
# A session acts as a workspace between your Python code and the database.
Sessionlocal = sessionmaker(autoflush = False, autocommit = False, bind = engine)

def getDB():
    db = Sessionlocal()
    
    try:
        yield db  # injects db into the route
    finally:
        db.close() # returns the connection to SQLAlchemy's connection pool

# Base
# declarative_base() creates a base class that lets SQLAlchemy automatically map your Python classes to database tables and keep track of their schema metadata.
Base = declarative_base()
