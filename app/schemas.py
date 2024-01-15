from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.sql import func


class StatusPedidoSchema(BaseModel):
    id: str | None = None
    numeropedido: int = 0
    timestamp : datetime | None = func.now()
    updatedAt : datetime | None = func.now()
    status : int = 1