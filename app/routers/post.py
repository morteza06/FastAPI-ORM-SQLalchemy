from .. import models, schemas, oauth2
from typing import List, Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)

# CRUD API code by $1.postgresql and $2.ORM 

# {{URL}}posts?limit=2&skip=1&search=new
# @router.get("/", response_model = List[schemas.Post])
@router.get("/", response_model = List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int =  Depends(oauth2.get_current_user), 
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    #   cursor.execute(""" SELECT * FROM posts """) 
    #   posts = cursor.fetchall()
    
    # print(limit)
    
    # posts = db.query(models.Post).filter(
    #     models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    # Design SQL Query in pgadmin and wirte with syntax join by queryset at the python
    # select posts.*, count(votes.post_id) as votes from posts Left outer join votes on posts.id = votes.post_id group by posts.id
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


# Creating posts
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int =  Depends(oauth2.get_current_user)):
# def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # this code no sql code and is ORM code by sqlalchemy
    #this is pydantic model       **  is a  unpack model here
    new_post = models.Post(owner_id=current_user.id, **post.dict()) #automatic unpack model here
    # (title=post.title, content=post.content, published=post.published)# <=  model
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    return new_post

# use this url for web http status = https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#client_error_responses
 
# Getting individual posts
@router.get("/{id}", response_model = schemas.PostOut )
def get_post(id: str, db: Session = Depends(get_db),
            current_user: int =  Depends(oauth2.get_current_user) ):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    
    # post=db.query(models.Post).filter(models.Post.id == id).first()
    
    # print(post)
    post= db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()
    
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with id:{id} was not found") # that is very cleaner
    return post

# Delete Post
 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),
                 current_user: int =  Depends(oauth2.get_current_user)):
    
    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s returning *""", (str(id),))
    
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()     

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")
    
    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
 
@router.put("/{id}", response_model = schemas.Post )
def update_post(id: int, updated_post: schemas.Post, db: Session = Depends(get_db),
                 current_user: int =  Depends(oauth2.get_current_user) ):
    # Postgres code
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s 
    #                RETURNING *""",
    #                (post.title, post.content, post.published, str(id) ) )
                   
    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id:{id} does not exist")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    # post_query.update({'title':'hey this is my updated title',  #hard code for test
                    #    'content': 'this is my updated content'},synchronize_session=False)
    post_query.update(updated_post.dict(), synchronize_session = False)
    
    db.commit()
    
    return post_query.first()