##-------------------------
## Imports
##-------------------------
#   -- Response is a FastAPI library class to manipulate the responses 
#   -- status is to name HTTP statuses without remebering the codes 
#      for instance status.HTTP_404_NOT_FOUND is a 404 when requested post item not found on my list 
#   -- HTTPException class will be used to raise HTTP Exceptions when needed.    
#    FastAPI       : Core 
#    Response      : Response Object class
#    status        : HTTP Statuses Constans: (Starlette Library feature. Installed FastAPI package)
#                    FastAPI is actually a sub-class of Starlette.#
#                    With FastAPI you get all of Starlette's features as FastAPI is just Starlette on steroids
#    HTTPException : HTTP Exceptions helper class
from fastapi import APIRouter, status, HTTPException 
from fastapi.params import Depends

#SQlAlchemy Library Dependencies
from sqlalchemy.orm.session import Session

##Import my app models and utils 
## --> see how I needed .. after from as these two py files are under a sub-folder of the app folder
#              ORM     DTOs      Authentication Helper
from .. import models, dtomodel, oauth2
from ..database import get_db

#Authentication helper  
#When I has the APIs on my main.py I just decorated my REST APIs with app.get, app.post, etc.
# since I moved the APIs to py files and placed then on the sub-folder api 
# I needed import APIRouter class from fastapi library, see import line 16 
# the replace all by @app with @router as @app will not work

#  #Define login routers --> IMPORTANT
#  Remember to Use posts APIs Router object in main.py  --> app.include_router(post.router)
router = APIRouter(
    prefix="/vote",
    tags=['Votes']  ##This is the tag for swagger to separate post related APIs in document in a section only for posts APIs
)

@router.post("/", status_code = status.HTTP_201_CREATED) 
## Previously I had this method declararion as below
#      async def create_post(post: dtomodel.PostCreateUpdate , db: Session= Depends(get_db)): 
#  It does not check for the user to be authenticated, below the new version, that requieres
#  the consumer of the PAI to be authenticated (provide the token) 
#  I will import my oauth2.py which is my helper for Authentication logic (see from .. import models, dtomodel, oauth2)
#  I then will inject my useir_id tourgh Authentication helper "get_current_user"
async def do_vote(vote: dtomodel.Vote, 
                      db: Session = Depends(get_db), 
                      #this is what forces the client process to be authenticated to be able to consume the endpoint 
                      # APIs
                      current_user: models.User = Depends(oauth2.get_current_user) ): 
    print("Vote: vote()")
    print("Voiting...") 

    #Check if post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with Id: {vote.post_id} does not exist.")

    vote_q = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.User.id == current_user.id)
    found_vote = vote_q.first()
    if vote.direction == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully!"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"Vote on post {vote.post_id} does not exist")
        vote_q.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully!"}
    print("Vote: vote() finished")
