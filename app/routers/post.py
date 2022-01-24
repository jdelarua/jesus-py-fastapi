##-------------------------
## Imports
##-------------------------
#Typing library (needed for the Response on get_all_posts() method that should return a List of Post )
from ntpath import join
from statistics import mode
from tokenize import group
from typing import List

#   -- Response is a FastAPI library class to manipulate the responses 
#   -- status is to name HTTP statuses without remebering the codes 
#      for instance status.HTTP_404_NOT_FOUND is a 404 when requested post item not found on my list 
#   -- HTTPException class will be used to raise HTTP Exceptions when needed.    
from fastapi import APIRouter, Response,  status, HTTPException 
#    FastAPI       : Core 
#    Response      : Response Object class
#    status        : HTTP Statuses Constans: (Starlette Library feature. Installed FastAPI package)
#                    FastAPI is actually a sub-class of Starlette.#
#                    With FastAPI you get all of Starlette's features as FastAPI is just Starlette on steroids
#    HTTPException : HTTP Exceptions helper class
#FastAPI Body class --> To read from Request Body
from fastapi.params import Depends

#SQlAlchemy Library Dependencies
from sqlalchemy.orm.session import Session
# import func from sqlalchemy needed for the count
from sqlalchemy import func


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
    prefix="/posts",
    tags=['Posts']  ##This is the tag for swagger to separate post related APIs in document in a section only for posts APIs
)


#############################
# POSTS related APIs 
#############################
#Implements REST GET method sample
#Route Decorator will force to return a List of dtomodel.PostVote  
#Route Decorator will force to return a List of dtomodel.PostVote  
@router.get("/", response_model=List[dtomodel.PostVote])  
#Route Decorator 
#     GET Request --> path: /posts   ----> See router = APIRouter(prefix="/posts") line 35
#Web api asynchroneous function get_posts() with DI
async def get_all_posts(db: Session= Depends(get_db),
                      #Request Query parameters
                      limit: int = 0,
                      skip: int = 0,
                      search: str = ""):      
    print(f"Posts: get_all_posts() / limit={limit}")
    #get posts from DB via SqlAlchemy ORM
     #if you print(db.query(models.Post)) you will see the SQL Statement (it is like the EF Linq expression)
    #SELECT * FROM POST LEFT OUTER JOIN VOTES ON POST.Id = VOTES.POST_ID 
    # func.count(models.Vote.id) will calculate the COUNT(*)
    # for this --> from sqlalchemy import func
    posts_q = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
                       models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id)
    '''
    #Above sqlalchemy statement will generate below query:
        SELECT posts.id AS posts_id, 
               posts.title AS posts_title, 
               posts.content AS posts_content, 
               posts.published AS posts_published, 
               posts.rating AS posts_rating, 
               posts.create_a       t AS posts_create_at, 
               posts.owner_id AS posts_owner_id, 
               count(votes.post_id) AS votes   ----> See .label("votes") on the sqlalquemy query
        FROM posts 
            LEFT OUTER JOIN votes ON posts.id = votes.post_id 
        GROUP BY posts.id
    '''
    #Filtering results by title?
    if search != "":
        #implemetig contains not case sencitive
        posts_q = posts_q.filter(models.Post.title.ilike(f"%{search}%"))
        #Case sencitive will be
        #  --> posts_q = posts_q.filter(models.Post.title.contains(search))
   
    # #Limiting results?
    if limit > 0:
        posts_q = posts_q.limit(limit)
    
    #Skipping rows?
    if skip > 0:
        posts_q = posts_q.offset(skip)

    print(posts_q)    
    posts = posts_q.all()

    print("Posts: get_all_posts() finished")
    return posts

@router.get("/user-posts", response_model=List[dtomodel.Post])  #Route Decorator 
#Route Decorator 
#     GET Request --> path: /posts/user-posts   ----> See router = APIRouter(prefix="/posts") line 35
async def get_user_posts(db: Session= Depends(get_db),
                         current_user: dtomodel.User = Depends(oauth2.get_current_user)
                         ):      
    print("Posts: get_user_posts()")
     #get posts from DB via SqlAlchemy ORM
     #if you print(db.query(models.Post)) you will see the SQL Statement (it is like the EF Linq expression)
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    print("Posts: get_user_posts() finished")
    return posts    

#Implements REST GET method sample with path parameters --> passing Id
#Route Decorator called with path paramter id
#     GET Request --> path: /posts/id   ----> See router = APIRouter(prefix="/posts") line 35
@router.get("/{id}", response_model=dtomodel.PostVote)     
async def get_one_post(id: int, res: Response, 
                       db: Session=Depends(get_db)): 
    print("Posts: get_one_post()")
#Web api asynchroneous function get_posts()
# I want to use FastAPI Repsonse to send back HTTP Statuses
    ###  --> post = db.query(models.Post).filter(models.Post.id == id).first()
    #To the above I want to get the Votes
    post = db.query(
                    models.Post, func.count(models.Vote.post_id).label("votes")
                   ).join(models.Vote, 
                          models.Post.id == models.Vote.post_id, 
                         isouter = True
                         ).group_by(
                                   models.Post.id
                                   ).filter(
                                            models.Post.id == id
                                   ).first()

    if not post: #is post null??? Set Status code 404 --> HTTP Not Found 
        #Code below works bu it is a little but sloppy, it is better to raise an HTTPException
        #  res.status_code = status.HTTP_404_NOT_FOUND
        #  return {"ERROR": f"Post with Id: {id} Not Found :("}
        #This code is much cleaner 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with Id: {id} Not Found :(")
    print("Posts: get_one_post() finished")
    return post

#Implements REST POST method sample
#Route Decorator 
#     POST Request --> path: /posts   ----> See router = APIRouter(prefix="/posts") line 35
 #Second parameter is the HTTP status code to return if post was successfully created 
 # Notice how create_post will render a Post pydantic model instead of a SqlAlchemy one
 #  See parameter: response_model=dtomodel.Post --> Best practices is to render the DTO instead of 
 #  an ORM model
@router.post("/", status_code = status.HTTP_201_CREATED, response_model=dtomodel.Post) 
## Previously I had this method declararion as below
#      async def create_post(post: dtomodel.PostCreateUpdate , db: Session= Depends(get_db)): 
#  It does not check for the user to be authenticated, below the new version, that requieres
#  the consumer of the PAI to be authenticated (provide the token) 
#  I will import my oauth2.py which is my helper for Authentication logic (see from .. import models, dtomodel, oauth2)
#  I then will inject my useir_id tourgh Authentication helper "get_current_user"
async def create_post(post: dtomodel.PostCreate, 
                      db: Session = Depends(get_db), 
                      #this is what forces the client process to be authenticated to be able to consume the endpoint 
                      # APIs
                      current_user: models.User = Depends(oauth2.get_current_user) ): 
    print("Posts: create_post()")
    print("Creating new Post >> Current User")                      
    print(current_user)                      
#Web api asynchroneous function create_post()  
    #Below approach was not so good as if we had many columns I would need to provide all of them
    #on my model.Post constructor to get the values from the pydantic model:
    #see below
    #    new_post = models.Post(
    #                  title=post.title, content=post.content, published=post.published, rating=post.rating)
    #Turns out I could convert my create_post (post: Post...) pypydantic model parameter as dict 
    # and then unpack the dict. watch how easy it is in ptyhon: 
    print("Creating new Post >> post details from client")                      
    print(post)     
    print("Do Update DB .....................")                 
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print("Posts: create_post() finished")
    return new_post

#Implements REST PUT method sample
#Route Decorator 
#     PUT Request --> path: /posts/id   ----> See router = APIRouter(prefix="/posts") line 35
@router.put("/{id}", response_model = dtomodel.Post) 
async def update_post(id: int, 
                      post: dtomodel.PostCreate, 
                      db: Session=Depends(get_db),
                      #this is what forces the client process to be authenticated to be able to consume the endpoint 
                      # APIs
                      current_user: dtomodel.User = Depends(oauth2.get_current_user),
                      ):
    print(f"Posts: update_post()")
    #Retrieve post to update from my Postgre Database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    upd_post = post_query.first()
    #check if Id exists by gettnig fisrt
    if  upd_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with Id: {id} Not Found :(")
    #Check user updating the post is the owner 
    if upd_post.owner_id != current_user.id:
        #Raise Forbbiden Error (403)!
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail= f"Post Update Denied :(")

    post_query.update(post.dict(), synchronize_session=False)                        
    #Finally commit updates
    db.commit()          
    #Why I had to do a post_query.first() again?
    #  Well truns out there is create_at column that is populated on the Server, we need to 
    #  retrieve that claculted value back, as I am not populating it on the client side.             

    print("Posts: update_post() finished")
    return post_query.first()

#Implements REST DELETE method sample
#Route Decorator 
#     DELETE Request --> path: /posts/id   ----> See router = APIRouter(prefix="/posts") line 35
#Second parameter is the HTTP status code to return if post was successfully created 
#When REST - DELETE API will return 204
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT) 
async def delete_post(id: int, 
                      db: Session=Depends(get_db),
                      #this is what forces the client process to be authenticated to be able to consume the endpoint 
                      # APIs
                      current_user: dtomodel.User = Depends(oauth2.get_current_user)):
    print("Posts: delete_post()")
    print(current_user)
    #to delete I just need the query expresion
    del_post_q = db.query(models.Post).filter(models.Post.id == id)
    del_post = del_post_q.first()
    #check if Id exists by gettnig fisrt
    if del_post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail= f"Post with Id: {id} Not Found :(")

    #Check user deleting the post is the owner 
    if del_post.owner_id != current_user.id:
        #Raise Forbbiden Error (403)!
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, 
                            detail= f"Post Deletion Denied :(")
    #Based on sqlalchemy docs below is the most efficient way to delete
    del_post_q.delete(synchronize_session=False)
    db.commit()

    print("Posts: delete_post() finished")
    #When 204 API should not return anything 
    return Response(status_code = status.HTTP_204_NO_CONTENT)