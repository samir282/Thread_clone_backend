from fastapi import FastAPI

from database import engine
from api.auth.model import auth_base
from api.routes.router import router

auth_base.metadata.create_all(bind = engine)

app = FastAPI()

app.include_router(router, prefix='/api')

