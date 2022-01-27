#############################################################
# To run this app
# From Terminal: 
#   > uvicorn app.main:app --reload
#############################################################
#Time module to call time class
# import time
#Typing library (needed for the Response on get_all_posts() method that should return a List of Post )
from operator import imod
from sqlalchemy.orm.session import Session
#########################################################
#API Support Framework --> FastAPI Library 
#For details about what you can get from FastAPI 
#  Go To: https://fastapi.tiangolo.com/features/
#########################################################
#Import FastAPI library
#   Got this sample from https://fastapi.tiangolo.com/tutorial/first-steps/ 

		##########################################################################################
		# THE BEAUTY OF FASTAPI LIBRARY IS THAT IT COMES WITH SWAGGER UI TO DOCUMENT YOUR APIS      #
		# URL IS:  MY APP URL: http://127.0.0.1:8000                                             #
		# WITH PATH /DOCS                                                                        #
		# SO:                                                                                    #
		#  http://127.0.0.1:8000/docs                                                            #
		#   or                                                                                   #
		#  http://127.0.0.1:8000/redoc  --> This is different form of documentation              #
		#                                   using tool called REDOC which is a React-based tool  #
		##########################################################################################
from fastapi import FastAPI 

#Handling CORS 
from fastapi.middleware.cors import CORSMiddleware

#Import routers for my Posts, User, Auth & Vote APIs 
from .routers import post, user, auth, vote

#############################################################
# App body
#############################################################
#Create database schema from SQLalchemy ORM models
#   (****) Sinde I switched to use Alembic I do not need my app to aut-generate database schema
#          I will use Alembic commands for migraitons
#   Code below "models.Base.metadata.create_all(bind=engine)" will be commented out:
#  
#    models.Base.metadata.create_all(bind=engine)   

#Create an instance of FastApi (FastApi is like Node --> Express)
app = FastAPI()

#Setup my app CORS plicy for origins --> Allow all origins to send requests to my app
#Origing is a list of string ex: ['https://google.com', 'https://youtube.com'] or "*" is all
origins = ["*"]

#Add CORS middleware CORSMiddleware include in FastAPI  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Below code moved to database.py
# #Keep app trying to connect if it fails
# while True:
#     try:
#     #Setup connection details
#     # -- As you can see we are harcoding DB info below, that is not good pratice. 
#     #    In the future, we will do this by reading from enviroment variables.
#         conn = psycopg2.connect(host='localhost',           #Server
#                             database='fastApi',             #Datbase
#                             user='postgres',                #Username
#                             password='sa',                  #Password
#                             cursor_factory=RealDictCursor   #Schema binding mappings (Requiered by this library)
#                             )
#         #Get schema inmemory cursor. This will allow me to execute SQL statements                       
#         cursor = conn.cursor()
#         print("PostgreSQl DB connection succeeded!")       
#         #If connection succeeded quick while                      
#         break
#     except Exception as err:
#         print("Connection Failed.")
#         print(f"Error: {err}")
#         #Wait 2 secs to try to connect again
#         time.sleep(2)

##########################
#### WIREUP ROTUTERS  ####
##########################
#Use Posts APIs Router object 
app.include_router(post.router)
#Use User APIs Router object 
app.include_router(user.router)
#Use Auth APIs Router object 
app.include_router(auth.router)
#Use Vote APIs Router object 
app.include_router(vote.router)

#Default route 
@app.get("/")
async def root():
	return {"message":"Welcome to Jesus Python API with FastApi!!!"}