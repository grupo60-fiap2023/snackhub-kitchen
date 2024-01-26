from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PW = os.environ.get("MYSQL_PW")
IP_APP = os.environ.get("IP_APP")
PORT = os.environ.get("PORT")

if os.environ.get("TESTING"):
    DATABASE_URL = "sqlite://"
    engine = create_engine(DATABASE_URL,
                    connect_args={'check_same_thread':False},
                    poolclass=StaticPool)
else:    
    DATABASE_URL = f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PW}@{IP_APP}:{PORT}/pedidos"
    print(DATABASE_URL)
    engine = create_engine(DATABASE_URL)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()