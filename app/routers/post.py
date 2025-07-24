from .. import models, schemas, oauth2
from fastapi import FastAPI,Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
from ..database import engine, get_db

router = APIRouter(
    prefix="/posts",
    tags = ['Posts'] #Tags used for proper documentation
)


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db), 
              current_user: int = Depends(oauth2.get_current_user), limit: int=50, skip: int=0, search: Optional[str]= ""):

    posts = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
             .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .filter(models.Post.title.contains(search)).group_by(models.Post.id).limit(limit).offset(skip).all()
    )
    # print("Results:", results)
    return posts
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # print(current_user.email) Get the current USER
    # print(current_user.id) Current user id
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)  
    db.commit()
    db.refresh(new_post)


    return new_post

@router.get("/{id}", response_model=schemas.PostOut) #{id} is a path parameter
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):


    post = (db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
            .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first())
    
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
   

    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()
    return post

@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #Deleting a post logic
    deleted_post = db.query(models.Post).filter(models.Post.id == id)
    post = deleted_post.first()

    if deleted_post.first() == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                    detail = f"post with id: {id} does not exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"User {current_user.id} not authorized to delete the post! ")
    
    deleted_post.delete(synchronize_session=False)
    db.commit()
   
   
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s WHERE id = %s RETURNING *""",
    #                (post.title,post.content,post.published, str(id),))
    # updated_post = cursor.fetchone()
    # connection.commit()
    if post == None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                    detail = f"post with id: {id} does not exist")
    
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post_query.first()


