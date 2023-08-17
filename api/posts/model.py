
from sqlalchemy import Column, String, DateTime, Uuid, ForeignKey, Integer
from sqlalchemy.orm import relationship

from database import base

post_base = base

class Post(post_base):
    __tablename__ = 'post'

    id = Column(Uuid, primary_key= True, nullable= False)
    user_name = Column(String(30), ForeignKey('user.user_name'))
    post_content = Column(String(120))
    post_time =  Column(DateTime)
    repost_ref_id = Column(Uuid, nullable= True)
    user = relationship('User', back_populates= 'post')
