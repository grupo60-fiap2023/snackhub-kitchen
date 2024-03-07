from app.database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ARRAY
from sqlalchemy.sql import func

class StatusPedido(Base):
    __tablename__ = "LogStatusPedido"
    id = Column(String(255), primary_key=True)
    numeropedido = Column(Integer, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    updatedAt = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())
    status = Column(Integer, nullable=False)
    itens = Column(String(255))