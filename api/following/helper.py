from fastapi import status, HTTPException
from sqlalchemy.orm import Session

from .model import Following

def follow_request(id : str, current_user , db : Session):
    try:
        user = db.query(Following).filter(Following.user_name == current_user.username and Following.following_id == id).first()
        if user:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= 'already following')
        f_user = Following(user_name = current_user.username,
                            following_id = id)
        db.add(f_user)
        db.commit()
        return{
            'details' : status.HTTP_201_CREATED,
            'message' : 'following'
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured: {e}')

def unfollow_request(id : str, current_user, db : Session):
    try:
        user = db.query(Following).filter(Following.user_name == current_user.username and Following.following_id == id).first()
        if not user:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= 'not following')
        db.delete(user)
        db.commit()
        return{
            'details' : status.HTTP_200_OK,
            'message' : 'Unfollowed'
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured: {e}')
    
def get_followers_details(current_user, db: Session):
    try:
        followers = db.query(Following).filter(Following.following_id == current_user.username).all()
        if not followers:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= 'No followers found')
        return followers
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured : {e}')
    
def get_following_details(current_user, db: Session):
    try:
        followings = db.query(Following).filter(Following.user_name == current_user.username).all()
        if not followings:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= 'Not following to anyone')
        return followings
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured : {e}')