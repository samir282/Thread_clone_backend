from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship

from database import base

following_base = base

class Following(following_base):
    __tablename__ = "following"

    id = Column(Integer, primary_key= True, index= True)
    user_name = Column(String(30), ForeignKey('user.user_name'))
    following_id = Column(String(30))
    user = relationship('User', back_populates= 'following')