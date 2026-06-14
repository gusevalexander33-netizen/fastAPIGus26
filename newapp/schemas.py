from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    fist_name: Optional[str] = None
    last_name: Optional[str] = None
    bio: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    bio: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_staff: bool
    date_joined: datetime

    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    slug: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class PostBase(BaseModel):
    title: str
    slug: str
    content: str
    category_id: Optional[int] = None
    status: str = 'draft'

class PostCreate(PostBase):
    author_id: int
    tag_id: Optional[List[int]]=[]

class PostUpdate(PostBase):
    title: Optional[str]=None
    content: Optional[str]=None
    status: Optional[str]=None
    category_id: Optional[int]=None

class PostResponse(PostBase):
    id: int
    author_id: int
    views_count: int
    created_at: datetime
    updated_at: Optional[datetime]=None
    published_at: Optional[datetime]=None

    class Config:
        from_attributes = True

class CommentBase(BaseModel):
    content: str
    post_id: int
    parent_id: Optional[int]=None

class CommentCreate(CommentBase):
    author_id: int

class CommentResponse(CommentBase):
    id: int
    author_id: int
    is_approved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str
    slug: str

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int

    class Config:
        from_attributes = True