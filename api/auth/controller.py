from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from .schema import User, login_schema
from database import get_db
from .helper import create_user, log_in
from .schema import Token

auth_router = APIRouter()

@auth_router.post('/signup', status_code= status.HTTP_201_CREATED)
def signup(request: User, db : Session = Depends(get_db)):
    return create_user(request.name, request.username, request.password, db)

@auth_router.post('/login', status_code= status.HTTP_200_OK, response_model= Token)
def login(request : login_schema, db : Session = Depends(get_db)):
    return log_in(request.username, request.password, db)