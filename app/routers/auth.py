#For my Auth router I will use below classes & methhods 
from fastapi import APIRouter, Depends, status, HTTPException, Response
#
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
#DAL using sqlalchemy orm
from sqlalchemy.orm import Session
from sqlalchemy.util.langhelpers import repr_tuple_names
#Get my current DB session from my Database class
from ..database import get_db     # ---> {database.py}
#for my UserLogin DTO
from .. import dtomodel, models   # ---> {dtomodel.py, models.py}
#To verify User password
from .. import utils              # ---> {utils.py}
#For JWT generation
from .. import oauth2             # ---> {oauth2.py}


#tags paramter is for swagger documentation 
#  --> tags paramter is a list of str so -> [] 

#  #Define Auth APIs Router --> IMPORTANT
#  Remember to Use Login APIs Router object in main.py  --> app.include_router(auth.router)
router = APIRouter(tags=["Authentication"])

@router.post("/login", response_model=dtomodel.Token)
## old --> async def login(user_credential: dtomodel.UserLogin, db: Session = Depends(get_db)):
## New --> I will inject OAuth2PasswordRequestForm class 
async def login(user_credential: OAuth2PasswordRequestForm=Depends(), db: Session = Depends(get_db)):
    print(">>> User logged in:")
    print(user_credential)

    #Search by user e-mail 
    # ** Since I am inecting from client OAuth2PasswordRequestForm class
    #    it has only username & apssword   
    ## old -->user = db.query(models.User).filter(models.User.email == user_credential.email).first()
    #using OAuth2PasswordRequestForm I need to compare to user_credential.username
    #*********************************************************************************************
    # Notice that when testing this API on Postman or Isomnia, use Form Data instead of body JSON 
    #*********************************************************************************************
    user = db.query(models.User).filter(models.User.email == user_credential.username).first()

    #HTTP_403_FORBIDDEN is the one used for Web APIs when user does not provide proper credentials
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    #HTTP_403_FORBIDDEN is the one used for Web APIs when user does not provide proper credentials
    if not utils.verifyPsw(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")

    #Create token (JWT)
    #data is the JWT payload I decided to use only user id
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    #Return Token
    #
    #"access_token": JWT 
    #"token_type"  : The token type. I will use "bearer" token type
    #To test your JWT go to jwt.io and paste the return access_token by this method
    return {"access_token":access_token, "token_type":"bearer"}

  




