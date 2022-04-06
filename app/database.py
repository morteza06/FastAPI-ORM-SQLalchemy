from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings
# https://fastapi.tiangolo.com/tutorial/sql-databases/?h=sql#create-the-sqlalchemy-parts
# 'postgresql://<username>:<password>@   <ip-address/hostname>  /<database_name>'
#Note: delete port part from URL

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:admin@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
        
        # hard code for conection 
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
#                                 password='admin', cursor_factory=RealDictCursor)  
#         # hard code is bad. no development save password database in there. 
#         # we need save dynamic in there
#         cursor = conn.cursor()
#         print("Databse connection was succesfull")
#         break
#     except Exception as error:
#         print("Connection to database failed")
#         print("Error: ",error)
#         time.sleep(2)