from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.sql import func
from typing import List



class StatusPedidoSchema(BaseModel):
    id: int = 0
    numeropedido: str = ""
    timestamp : datetime = func.now()
    updatedAt : datetime = func.now()
    status : int = 5
    itens : str = ""