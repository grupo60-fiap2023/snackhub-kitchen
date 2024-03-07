from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.sql import func
from typing import List



class StatusPedidoSchema(BaseModel):
    id: str = "None"
    numeropedido: int = 0
    timestamp : datetime = func.now()
    updatedAt : datetime = func.now()
    status : int = 1
    itens : List[str] = None