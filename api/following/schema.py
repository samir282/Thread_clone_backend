from pydantic import BaseModel


class Followers(BaseModel):
    user_name : str