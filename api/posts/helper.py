from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import uuid
import datetime
import math
from uuid import UUID

from .model import Post
from ..following.model import Following

def post_blog(blog : str, db : Session, current_user):
    try:
        post = Post(id = uuid.uuid4(),
                    user_name = current_user.username,
                    post_content = blog,
                    post_time = datetime.datetime.now())
        db.add(post)
        db.commit()
        return {
            'post_id' : post.id,
            'message' : "posted",
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occured{e}')
    
def delete_a_post(id1 : UUID, current_user, db : Session):
    try:
        post = db.query(Post).filter(Post.user_name == current_user and Post.id == id1).first()
        if not post:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail='You r not authorized to delete this post')
        db.delete(post)
        db.commit()
        return {
            'status' : status.HTTP_200_OK,
            'details' : 'Post deleted'
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'an error occured: {e}')

def get_profile_timeline(user_id: str, current_user: str, page: int , limit: int , db: Session):
    try:
        offset = (page - 1) * limit
        timeline = db.query(Post).filter(Post.user_name == user_id).order_by(Post.post_time.desc()).offset(offset).limit(limit).all()

        total_post = db.query(Post).filter(Post.user_name == current_user).count()
        total_pages = math.ceil(total_post/limit)
        print(total_post, total_pages)
        if page>total_pages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'No more post available')
        if not timeline:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Nothing posted yet')
        return timeline
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occurred: {e}')

def get_user_timeline(current_user: str, page  : int, limit : int, db : Session):
    try:
        offset = (page-1) * limit
        timeline = db.query(Post)\
              .join(Following, Post.user_name == Following.following_id)\
              .filter(Following.user_name == current_user).order_by(Post.post_time.desc()).offset(offset).limit(limit).all()
        total_post = db.query(Post)\
              .join(Following, Post.user_name == Following.following_id)\
              .filter(Following.user_name == current_user).count()
        total_pages = math.ceil(total_post/limit)
        print(total_post, total_pages)
        if page>total_pages or not timeline:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'No post available')
        return timeline
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occurred: {e}')