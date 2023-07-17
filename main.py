from fastapi import FastAPI


from database import engine
from api.auth.model import auth_base
from api.following.model import following_base
from api.routes.router import router

auth_base.metadata.create_all(bind = engine)
auth_base.metadata.create_all(bind = engine)

app = FastAPI()

# @AuthJWT.load_config
# def get_config():
#     return Settings()

app.include_router(router, prefix='/api')

