### jose JWT handling library
import re
import fastapi
from fastapi.param_functions import Depends
from fastapi.security import oauth2
from fastapi.security.oauth2 import OAuth2
from fastapi import status, HTTPException
from jose import jwt, JWTError
### Datetime to setup token expiration time
from datetime import datetime, timedelta
###            DTO &    ORM Entity Model
from . import dtomodel, models
### Oauth2 Schema
from fastapi.security import OAuth2PasswordBearer
#Import Session Object from SQlalchemy
from sqlalchemy.orm  import Session
#DAL
from . database import get_db

#import my app config 
from .config import settings


##End Point Web API route (/login) --> When passing as tokenUrl just remove the slash 
## oauth2_scheme will be injected to my get_current_user()  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#To get this working I need to provide: (See example @ https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
#SECRET_KEY   (Arbitrary long test)
SECRET_KEY  = settings.secret_key
#ALGORITHM
ALGORITHM = settings.algorithm
#TOKEN EXPIRATION TIME
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expiration_minutes #change to 30, once tested expiration with 1 min 

def create_access_token(data: dict):
    #make a copy of the received dictionary, so we do not lose it
    to_encode =data.copy()
    #provide expiration time remenber to use utcnow()
    expire = datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    #dict.update() will add a new key pair value to the dictionary if the key does not exist
    #if key exists it will update the value
    to_encode.update({"exp": expire})
    # claims   : What you want to put on the JWT payload
    # key      : SECRET_KEY
    # algorithm: LGORITHM
    encoded_jwt =jwt.encode(claims=to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = dtomodel.TokenData(id=id) 
    except JWTError as e:
        #Display error on the conosle
        print(e)
        raise credentials_exception
    # except AssertionError as e:
    #     #Display error on the conosle
    #     print(e)

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session=Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
    detail=f"Could not validate Credentials", 
    headers={"WWW-Authenticate":"Bearer"})
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user

