#############################
# USER related APIs 
#############################
##-------------------------
## Imports
##-------------------------
#Time module to call time class
import time
#Typing library (needed for the Response on get_all_posts() method that should return a List of Post )
from typing import List

#   -- Response is a FastAPI library class to manipulate the responses 
#   -- status is to name HTTP statuses without remebering the codes 
#      for instance status.HTTP_404_NOT_FOUND is a 404 when requested post item not found on my list 
#   -- HTTPException class will be used to raise HTTP Exceptions when needed.    
from fastapi import FastAPI, APIRouter, Response, routing, status, HTTPException 
#    FastAPI       : Core 
#    Response      : Response Object class
#    status        : HTTP Statuses Constans: (Starlette Library feature. Installed FastAPI package)
#                    FastAPI is actually a sub-class of Starlette.#
#                    With FastAPI you get all of Starlette's features as FastAPI is just Starlette on steroids
#    HTTPException : HTTP Exceptions helper class
#FastAPI Body class --> To read from Request Body
from fastapi.params import Body, Depends

#SQlAlchemy Library Dependencies
from sqlalchemy.orm.session import Session

##Import my app models and utils 
## --> see how I needed .. after from as these two py files are under a sub-folder of the app folder
from .. import models, dtomodel, utils
from ..database import get_db

#When I has the APIs on my main.py I just decorated my REST APIs with app.get, app.post, etc.
# since I moved the APIs to py files and placed then on the sub-folder api 
# I needed import APIRouter class from fastapi library, see import line 16 
# the replace all by @app with @router as @app will not work

#  #Define user routers --> IMPORTANT
#  Remember to Use posts APIs Router object in main.py  --> app.include_router(user.router)
router = APIRouter(
    prefix="/users",
    tags=['Users'] ##This is the tag for swagger to separate user related APIs in document in a section only for user APIs

)

###############
#APIs
###############
#Route Decorator 
#     GET Request --> path: /users  ----> See router = APIRouter(prefix="/users") line 38
@router.get("/", response_model=List[dtomodel.User])  
async def get_all_users(db: Session= Depends(get_db)):      
    users = db.query(models.User).all()
    return users

@router.get("/{id}", response_model=dtomodel.User)  
async def get_one_users(id: int, db: Session= Depends(get_db)):      
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"User with Id: {id} Not Found :(")
    return user

@router.post("/", status_code = status.HTTP_201_CREATED, response_model=dtomodel.User) 
async def create_user(user: dtomodel.UserCreateUpdate , db: Session= Depends(get_db)): 
    #Hash user poassword
    #update my pydantic user mode password property to the encypted one
    user.password = utils.hash_text(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.put("/{id}", response_model=dtomodel.User) 
async def update_post(id: int, 
                      user: dtomodel.UserCreateUpdate, 
                      db: Session=Depends(get_db)):
    #to delete I just need the query expresion
    user_query = db.query(models.User).filter(models.User.id == id)
    upd_user = user_query.first()
    #check if Id exists by gettnig fisrt
    if  upd_user == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail= f"User with Id: {id} Not Found :(")
    user_query.update(user.dict(), synchronize_session=False)                        
    #Finally commit updates
    db.commit()          
    return user_query.first()