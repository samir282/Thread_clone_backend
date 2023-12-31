from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..auth.schema import User
from ..auth.utils import get_current_user
from database import get_db
from .helper import follow_request, unfollow_request, get_followers_details, get_following_details
from .schema import Followers, Following



f_router = APIRouter()

@f_router.post("/follow/{id}", status_code= status.HTTP_202_ACCEPTED)
def follow(id : str, current_user : User = Depends(get_current_user),db : Session = Depends(get_db)):
    return follow_request(id, current_user, db)

@f_router.post("/unfollow/{id}", status_code= status.HTTP_200_OK)
def unfollow(id : str, current_user : User = Depends(get_current_user),db : Session = Depends(get_db)):
    return unfollow_request(id, current_user, db)

@f_router.post("/followers", status_code= status.HTTP_200_OK, response_model= list[Followers])
def get_followers(current_user : User = Depends(get_current_user),db : Session = Depends(get_db)):
    return get_followers_details(current_user, db)

@f_router.post("/followings", status_code= status.HTTP_200_OK, response_model=list[Following])
def get_followings(current_user : User = Depends(get_current_user),db : Session = Depends(get_db)):
    return get_following_details(current_user, db)