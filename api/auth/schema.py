from pydantic import BaseModel

class User(BaseModel):
    name : str
    username : str
    password : str

class login_schema(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

