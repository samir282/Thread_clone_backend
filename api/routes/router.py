from fastapi import APIRouter

from ..auth.controller import auth_router
from ..posts.controller import post_router

router = APIRouter()

router.include_router(
    auth_router,
    prefix= "/auth",
    tags= ["AUth"]
)

router.include_router(
    post_router,
    prefix= "/post",
    tags= ["Post"]
)