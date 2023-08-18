from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import uuid
import datetime
import math
from uuid import UUID

from .model import Post, Like
from ..following.model import Following

def post_blog(blog : str, db : Session, current_user):
    try:
        post = Post(id = uuid.uuid4(),
                    user_name = current_user.username,
                    post_content = blog,
                    post_time = datetime.datetime.now(),
                    total_like = 0
                    )
        
        db.add(post)
        db.commit()
        return {
            'post_id' : post.id,
            'message' : "posted"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occured{e}')
    
def getpost(post_id, db):
    try:
        post = db.query(Post).filter(post_id == Post.id).first()
        if not post:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="post not found")
        return post
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occured{e}')
    
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
        total_post = db.query(Post).filter(Post.user_name == current_user).count()
        total_pages = math.ceil(total_post/limit)
        print(total_post, total_pages)
        if page>total_pages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'No more post available')
        offset = (page - 1) * limit
        timeline = db.query(Post).filter(Post.user_name == user_id).order_by(Post.post_time.desc()).offset(offset).limit(limit).all()
        if not timeline:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No Post available')
        return timeline
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occurred: {e}')

def get_user_timeline(current_user: str, page  : int, limit : int, db : Session):
    try:
        total_post = db.query(Post)\
              .join(Following, Post.user_name == Following.following_id)\
              .filter(Following.user_name == current_user).count()
        total_pages = math.ceil(total_post/limit)
        print(total_post, total_pages)
        if page>total_pages:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'No post available')
        offset = (page-1) * limit
        timeline = db.query(Post)\
              .join(Following, Post.user_name == Following.following_id)\
              .filter(Following.user_name == current_user).order_by(Post.post_time.desc()).offset(offset).limit(limit).all()
        if not timeline:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= 'No post available')
        return timeline
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occurred: {e}')
    
def re_post(post_id, blog, current_user, db):
    try:
        post = Post(
                    id = uuid.uuid4(),
                    user_name = current_user,
                    post_content = blog,
                    post_time = datetime.datetime.now(),
                    repost_ref_id = post_id
                    )
        db.add(post)
        db.commit()
        return {
            'post_id' : post.id,
            'message' : "posted"
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occured{e}')
    
def reposts(post_id, db):
    try:
        reposts = db.query(Post).filter(post_id == Post.repost_ref_id).all()
        if not reposts:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="No repost found")
        return reposts
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'an error occured{e}')
    
def like_unlike_post(post_id: UUID, curent_user, db : Session):
    try:
        islike = db.query(Like).filter(curent_user == Like.liked_user_name and post_id== Like.post_id).first()
        post = db.query(Post).filter(post_id == Post.id).first()
        if islike:
            post.total_like -=1
            db.delete(islike)
            db.commit()
            return{
                'message' : 'unliked',
                'total_like' : post.total_like
            }
        else:
            like = Like(
                        post_id = post_id,
                        liked_user_name = curent_user
                        )
            post.total_like +=1
            db.add(like)
            db.commit()
            return {
                'message' : "liked",
                'total_like' : post.total_like
            }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'an error occured{e}')