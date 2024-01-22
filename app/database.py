from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os
#URL pra testar em memória usando sqlite.
#DATABASE_URL = "sqlite://"

if os.environ.get("TESTING"):
    DATABASE_URL = "sqlite://"
    engine = create_engine(DATABASE_URL,
                    connect_args={'check_same_thread':False},
                    poolclass=StaticPool)
else:
    #URL para acessar o banco pela imagem (produção)
    #DATABASE_URL = "mysql+mysqlconnector://root:123456@snackhub-mysql-db-kitchen:3306/pedidos"
    #URL para acessar pelo VSCode (debug)
    DATABASE_URL = "mysql+mysqlconnector://root:123456@localhost:3307/pedidos"
    engine = create_engine(DATABASE_URL)



SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()