from pydantic import BaseModel
from datetime import datetime


class post_schema(BaseModel):
    blog : str


class Timeline(BaseModel):
    user_name : str
    post_content: str
    post_time : datetime

