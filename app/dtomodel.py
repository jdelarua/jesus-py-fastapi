#########################################################
#Python Types package
#########################################################
#Used to declare create_at field
from datetime import datetime
#Used to declare optinal fields
from typing import Optional
#############################################################
#APIs Request Data Parsing * Validations --> Pydantic Library
#############################################################
#Pydantic library BaseModel to validate expected schema with what comes from request
#Pydantic features we get from FastAPI Library as well
#   With FastAPI you get all of Pydantic's features as FastAPI is based on Pydantic for all the data handling
#Pydantic --> https://pydantic-docs.helpmanual.io/
from pydantic import BaseModel, EmailStr, conint

##########################
#Users Models
##########################
class UserBase(BaseModel): 
    email   : EmailStr  #<- Pydantic datatype to check e-mals to be a valid e-mail format
    password: str

class UserCreateUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    create_at: Optional[datetime] = None 
    class Config:
        orm_mode = True  

#for my Auth router
class UserLogin(UserBase):
    pass

#Define Schema for my Access Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

##########################
#Posts Models
##########################
#Post classes to validate createpost request schema coming form the wire
#Below python class declaration means that my Post class extends BaseModel class
#Remember BaseModel class is on "pydantic" library
#Pydantic model to validade API Requests Posts parameters
class PostBase(BaseModel): 
    title    : str         
    content  : str         
    rating   : int 
    published: bool = True
    owner_id : int        

class PostCreate(PostBase): 
    pass

class Post(PostBase):
    id: int
    create_at: Optional[datetime] = None 
    owner: User
    #Based on  Pydantic library documentation below is needed to map SqlAlchemy ORM model to a Pydantic model
    #as I cam reshape the respopnse model to return whatever I want
    #In my API I render a pydantic model
    class Config:
        orm_mode = True    


##########################
#Vote Model
##########################
class Vote(BaseModel):
    post_id: int
    #Pydantic integer constrained to be >=0 && <=1
    direction: conint(ge=0, le=1)



###################################################################
#Post - Vote Model
###################################################################
#In my get_all_posts() from post.py 
# Sqlalchemy return below object structure
#  {
#     "Post": {
#         "content": "Content for Post 2X9 (6)",
#         "title": "Post 2X9 - Owner  (6)",
#         "rating": 99,
#         "owner_id": 6,
#         "published": true,
#         "create_at": "2022-01-15T15:06:14.831242-05:00"
#         "id": 41,
#     },
#     "votes": 2
# },
# So I will define a pydantic model DTO that matches the structure  
###################################################################
class PostVote(BaseModel):
    Post: Post
    votes: int
    
    class Config:
        orm_mode = True    

