import app.schemas as schemas, app.models as models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db
from sqlalchemy.sql import func
from sqlalchemy import Table, MetaData, Column, DateTime, String, Integer, update

metadata = MetaData()

pedidos = Table(
   'LogStatusPedido', metadata, 
   Column('id', String(255), primary_key=True),
   Column('numeropedido', Integer),
   Column('timestamp', DateTime(timezone = True), server_default=func.now()), 
   Column('updatedAt', DateTime(timezone = True), server_default=func.now(), onupdate=func.now()),
   Column('status', Integer)
)

router = APIRouter()

@router.post("/criar_pedido", status_code=status.HTTP_201_CREATED)
async def criar_pedido(pedido: schemas.StatusPedidoSchema, db: Session = Depends(get_db)):
    # Criar uma nova sessão
    try:
        new_pedido = models.StatusPedido(**pedido.dict())
        db.add(new_pedido)
        db.commit()

        db.refresh(new_pedido)
        return {"message": "Pedido criado com sucesso"}        
    except Exception as e:
        # Reverter as mudanças em caso de erro
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao registrar pedido: {e}")

@router.put("/statusempreparacao/{idPedido}")
async def atualizar_status_em_preparacao(idPedido : str, db: Session = Depends(get_db)):
    return await AtualizarStatus(idPedido, 2, db)

@router.put("/statuspronto/{idPedido}")
async def atualizar_status_pronto(idPedido : str, db: Session = Depends(get_db)):
    return await AtualizarStatus(idPedido, 3, db)

@router.put("/statusfinalizado/{idPedido}")
async def atualizar_status_finalizado(idPedido : str, db: Session = Depends(get_db)):
    return await AtualizarStatus(idPedido, 4, db)

async def AtualizarStatus(idPedido : str, status: int, db: Session):
    get_query = db.query(models.StatusPedido).filter(models.StatusPedido.id == idPedido)
    pedido_result = get_query.first()

    if not pedido_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Pedido numero {idPedido} não encontrado"
        )
    if pedido_result.status +1 != status:
         raise HTTPException(status_code=400, detail=f"Pedido {idPedido} não pode mudar para o status {status}")
    try:
        update_query = update(pedidos).where(pedidos.columns.id == idPedido).values(
                    status=status
                )
        result = db.execute(update_query)
        db.commit()
        if result.rowcount ==0:
                    raise HTTPException(status_code=400, detail="Erro ao atualizar status do produto.")
        return {"Message": "Atualização de status criado com sucesso"}
    except Exception as e:
                db.rollback()
                raise HTTPException(status_code=400, detail=f"Erro ao atualizar status do produto: {e}")

@router.get("/pedidos/{status}")
async def obter_pedidos_por_status(status : int, db: Session = Depends(get_db)):
    result = (
         db.query(models.StatusPedido)
         .filter(models.StatusPedido.status == status)
         .all()
    )
    return {"Status" : "Success", "Results" : len(result), "Pedidos" : result}