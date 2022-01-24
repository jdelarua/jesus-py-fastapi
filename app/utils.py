#Utility Module
#User Password Encryption libraries
from passlib.context import CryptContext

#Setup my password encryption context
#We are using bcrypt encryption algorythm
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_text(text: str):
    return  pwd_context.hash(text)

def verifyPsw(plain_psw, hashed_psw):
    return pwd_context.verify(plain_psw, hashed_psw)


