from fastapi import APIRouter, status, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from .schema import post_schema, Timeline
from database import get_db
from .helper import post_blog
from ..auth.schema import User
from ..auth.utils import get_current_user
from .helper import get_profile_timeline, get_user_timeline, delete_a_post, re_post, reposts, getpost

post_router = APIRouter()

@post_router.post("/post", status_code= status.HTTP_201_CREATED)
def post(request : post_schema, current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    return post_blog(request.blog, db, current_user)

@post_router.get("/get_post/{post_id}", status_code= status.HTTP_200_OK, response_model= Timeline)
def get_post(post_id : UUID, db : Session= Depends(get_db), current_user : User = Depends(get_current_user)):
    return getpost(post_id, db)

@post_router.delete("/delete/{id}", status_code= status.HTTP_202_ACCEPTED)
def delete_post(id : UUID, current_user : User = Depends(get_current_user), db : Session = Depends(get_db)):
    return delete_a_post(id , current_user.username, db)

@post_router.post("/profile_timeline/{id}", status_code= status.HTTP_200_OK)
def profile_timeline(user_id: str, page: int = Query(1, ge=1),
                  limit: int = Query(10, ge=1, le=100),
                  current_user : User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    # x = get_profile_timeline(user_id, current_user.username, page, limit, db)
    # return x
    return get_profile_timeline(user_id, current_user.username, page, limit, db)

@post_router.post("/user_timeline", status_code= status.HTTP_200_OK, response_model= List[Timeline])
def user_timeline(page : int = Query(1, ge= 1),
                  limit : int = Query(10, ge= 1, le= 100),
                  current_user : User = Depends(get_current_user),
                  db : Session = Depends(get_db)):
    return get_user_timeline(current_user.username, page, limit, db)

@post_router.post("/repost/{id}", status_code= status.HTTP_201_CREATED)
def repost(post_id : UUID, request : post_schema, db : Session= Depends(get_db), current_user : User = Depends(get_current_user)):
    return re_post(post_id, request.blog,current_user.username,db)

@post_router.get("/get_reposts",status_code= status.HTTP_200_OK, response_model= List[Timeline])
def get_reposts(post_id : UUID, db : Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    return reposts(post_id, db)

