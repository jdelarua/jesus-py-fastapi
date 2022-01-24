##Copy paste from SqlAchemy documentation: https://fastapi.tiangolo.com/tutorial/sql-databases/
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#Import Session Object from SQlalchemy
from sqlalchemy.orm  import Session
from sqlalchemy.sql.expression import false

#Time module to call time class
import time


#############################################################
#DataAccess --> psycopg2 library
#*****************************************************
#  (*) THIS IS NOT NEEDED WHEN USING SQLALCHEMY ORM  -->  psycopg2
#*****************************************************
#############################################################
#Import psycopg2 library as my middleware connect to PostgreSql  
import psycopg2
#Database Schema binding with client side (mappings). This is requiered by psycopg library
from psycopg2.extras import RealDictCursor

#import my app config 
from .config import settings

#ConnectionString
#Postgres driver format  --> postgresql://user:password@postgresserver/db
#  old not using pydantic env setting -->SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:sa@localhost/fastApi'
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
#Create the Sqlalchemy engine. Engine is the resposible to connect to my Postres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Define my connection session
SessionLocal  = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Define Models Base Class
Base = declarative_base()

# not used as we are using SQLAchemy ORM
# def db_connect():
#     #Keep app trying to connect if it fails
#     while True:
#         try:
#             #Setup connection details
#             # -- As you can see we are harcoding DB info below, that is not good pratice. 
#             # In the future, we will do this by reading from enviroment variables.
#             conn = psycopg2.connect(host='localhost',           #Server
#                             database='fastApi',             #Datbase
#                             user='postgres',                #Username
#                             password='sa',                  #Password
#                             cursor_factory=RealDictCursor   #Schema binding mappings (Requiered by this library)
#                             )
#             #Get schema inmemory cursor. This will allow me to execute SQL statements                       
#             cursor = conn.cursor()
#             print("PostgreSQl DB connection succeeded!")       
#             #If connection succeeded quick while                      
#             break
#         except Exception as err:
#             print("Connection Failed.")
#             print(f"Error: {err}")
#             #Wait 2 secs to try to connect again
#             time.sleep(2)



#Dependency Injection
#Below logic will create the Session Object inject to th caller function. 
#on each request, when the request fulfilled session will be closed
def get_db():
    db = SessionLocal()
    try:
        print("get_db YIELD")
        yield db
    finally:
        print("get_db Close")
        db.close()
