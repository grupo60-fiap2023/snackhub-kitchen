from pydantic import BaseModel
from datetime import datetime

class StatusPedidoSchema(BaseModel):
    id: str | None = None
    numeropedido: int = 0
    timestamp : datetime | None = None
    updatedAt : datetime | None = None
    status : int = 1