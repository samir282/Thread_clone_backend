from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

from .model import User
from api.auth.utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

def create_user(name:str, user_name: str, password: str, db: Session):
    try:
        user = db.query(User).filter(User.user_name == user_name).first()

        if user:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= "user already exist")
        
        user = User(full_name = name,
                    user_name = user_name,
                    password = generate_password_hash(password))
        
        db.add(user)
        db.commit()
        return{
            'details' : 'user created',
            'id' : user.user_name
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured: {e}')

def log_in(username,password, db : Session):
    try:
        db_user = db.query(User).filter(User.user_name == username).first()

        if db_user and check_password_hash(db_user.password, password):
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = create_access_token(data={"sub": db_user.user_name}, expires_delta=access_token_expires)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, detail= 'Invalid username or password')
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code= status.HTTP_500_INTERNAL_SERVER_ERROR, detail= f'An error occured: {e}')
