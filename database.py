from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


dbURL = "mysql://root:root@localhost:3306/threads"

engine = create_engine(dbURL)

session_local = sessionmaker(autocommit = False,bind = engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()

base = declarative_base()



