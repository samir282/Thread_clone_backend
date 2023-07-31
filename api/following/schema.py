from pydantic import BaseModel


class Followers(BaseModel):
    user_name : str

class Following(BaseModel):
    following_id : str