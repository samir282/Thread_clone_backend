from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship

from database import base

auth_base = base
class User(auth_base):
    __tablename__ = 'user'

    full_name = Column(String(255))
    user_name = Column(String(255), unique= True, primary_key= True)
    password = Column(Text,nullable=False)
    following = relationship('Following', back_populates= 'user')
    post = relationship('Post', back_populates= 'user')