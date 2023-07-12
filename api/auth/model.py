from sqlalchemy import Column, String

from database import base

auth_base = base
class User(auth_base):
    __tablename__ = 'user'

    user_name = Column(String(255), unique= True, primary_key= True)
    password = Column(String(30))
    Full_name = Column(String(255))