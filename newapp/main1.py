from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional, List
import uvicorn

import models
import schemas
import crud
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Django FastAPI",
    description="API 1task",
    version="1.0.0"
)
@app.get("/api/users/", response_model=List[schemas.UserResponse], tags=["Users"])
def get_users(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        db: Session = Depends(get_db),
):
    """GET - get all users"""
    users = crud.get_users(db, skip=skip, limit=limit)
    return users
@app.get("/api/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    """GET - get user by id"""
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
@app.post("/api/users/", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED, tags=["Users"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """POST - create new user"""
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = crud.get_user_by_username(db, username=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    return crud.create_user(db=db, user=user)
@app.put("/api/users/{user_id}", response_model=schemas.UserResponse, tags=["Users"])
def update_user(
        user_id: int,
        user: schemas.UserUpdate,
        db: Session = Depends(get_db)
):
    """PUT - update user data"""
    db_user = crud.update_user(db, user_id=user_id, user_update=user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
@app.delete("/api/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """DELETE - delete user"""
    db_user = crud.delete_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return None
@app.get("/api/posts/", response_model=List[schemas.PostResponse], tags=["Posts"])
def get_posts(
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100),
        status_filter: Optional[str] = Query(None),
        db: Session = Depends(get_db)
):
    """GET - get all posts with status"""
    return crud.get_posts(db, skip=skip, limit=limit, status=status_filter)

@app.get("/api/posts/{post_id}", response_model=schemas.PostResponse, tags=["Posts"])
def get_post(post_id: int, db: Session = Depends(get_db)):
    """GET - get post by id"""
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
@app.post("/api/posts/", response_model=schemas.PostResponse, status_code=status.HTTP_201_CREATED, tags=["Posts"])
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """POST - create new post"""
    author = crud.get_user(db, user_id=post.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return crud.create_post(db=db, post=post)
@app.put("/api/posts/{post_id}", response_model=schemas.PostResponse, tags=["Posts"])
def update_post(
        post_id: int,
        post: schemas.PostUpdate,
        db: Session = Depends(get_db)
):
    """PUT - update post"""
    db_post = crud.update_post(db, post_id=post_id, post_update=post)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post
@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Posts"])
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """DELETE - delete post"""
    db_post = crud.delete_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return None
@app.get("/api/health/", tags=["System"])
def health_check():
    """Health check"""
    return {"status": "healthy", "message": "API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)



