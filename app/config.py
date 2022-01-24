#Import pydantic BaseSettings class 
from pydantic import BaseSettings

#############################################################################
# Class to store all settings my app will use in a pydantic model
#   BaseSetting is usefull b/c it will try to macth Windows environmental 
#   varibles to the name of defined property, meaning that it will set
#   Settings property mapped to enviromental variables that match  
#   the name of the property
#   pydantic BaseSetting class also read from .env files
#   as it uses python-dotenv library features to read environmental variables
#   from a .env file 
#############################################################################
class Settings(BaseSettings):
    #Database Connection Related Setttings
    database_hostname: str 
    database_port: str 
    database_name: str 
    database_username: str 
    database_password: str 
    #JWT Token Related Setttings
    secret_key: str 
    algorithm: str 
    access_token_expiration_minutes: int 
    
    class Config:
        env_file = ".env"
        
        
settings = Settings()
