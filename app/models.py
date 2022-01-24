#Import SQlAchemy base model class
import sqlalchemy
from .database import Base
#Import SqlAlchemy  Columns definitions and datatypes
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, TIMESTAMP
#Expressions for --> create_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
from sqlalchemy.sql.expression import text
#For relationship method --> EF Navigation Properties like
from sqlalchemy.orm import relationship

#My Post class extends SQLalchemy Base model  class
#SQLalchemy Models

# =======================================================
# IMPORTANT NOTE about SQLalchemy and schema changes:
# =======================================================
# It would create the table objects form below models only if the do not exit.
# for table alter when they exist for this purpose we will need a spcific database migration tool
# called Alembic
#Post Model
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    rating = Column(Integer, nullable=False, server_default="0")
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)
    #define  posts_orm.owner_id as a FK to users_orm.id
    owner_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), nullable=False)

    #EF Navigation property like for Tables Relationships
    #relationship() returns an instance of the class for the model provided as paramter
    # in this case User class
    # (***) Notice how I am passing not the name of the table but the SqlAlchemy Class
    owner = relationship("User")  ##<-- Like in EF you provide the name of the Class instead of the table


#User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)

#Votes
class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey('users.id',ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id',ondelete="CASCADE"), primary_key=True, nullable=False)


