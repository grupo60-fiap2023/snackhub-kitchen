import app.schemas as schemas, app.models as models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter
from app.database import get_db
import json
from app.messages import enviar_mensagem_saida


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

@router.put("/statusempreparacao/{id_pedido}")
async def atualizar_status_em_preparacao(id_pedido : str, db: Session = Depends(get_db)):
    return await atualizar_status(id_pedido, 6, db)

@router.put("/statusfinalizado/{id_pedido}")
async def atualizar_status_finalizado(id_pedido : str, db: Session = Depends(get_db)):
    return await atualizar_status(id_pedido, 7, db)

async def atualizar_status(id_pedido : str, status: int, db: Session):
    get_query = db.query(models.StatusPedido).filter(models.StatusPedido.id == id_pedido)
    pedido_result = get_query.first()

    if not pedido_result:
        raise HTTPException(status_code=404, detail = f"Pedido numero '{id_pedido}' não encontrado")
    if pedido_result.status +1 != status:
         raise HTTPException(status_code=400, detail=f"Pedido '{id_pedido}' não pode mudar para o status {status}. Status do pedido: {pedido_result.status}")
    payload = schemas.StatusPedidoSchema()
    payload.status = status

    try:
        update_data = payload.dict(exclude_unset=True)
        get_query.filter(models.StatusPedido.id == id_pedido).update(
            update_data, synchronize_session=False
        )
        db.commit()
        db.refresh(pedido_result)

        map_status = {
            "6" : "IN_PREPARATION",
            "7" : "FINISHED"
        }
        stat = "Padrao"
        if str(status) in map_status:
        # Retorna o valor correspondente no dicionário
            stat = map_status[str(status)]
        reg = {
            "order-id" : id_pedido,
            "status" : stat 
        }

        json_string = json.dumps(reg)

        enviar_mensagem_saida(json_string)

        success_message = f"Pedido '{id_pedido}' atualizado com sucesso"
        return {"message": success_message}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao atualizar status do produto: {e}")

@router.get("/pedidos/{status}")
async def obter_pedidos_por_status(status : int, db: Session = Depends(get_db)):
    result = (
         db.query(models.StatusPedido)
         .filter(models.StatusPedido.status == status)
         .order_by(models.StatusPedido.timestamp.desc())
         .limit(10)
         .all()
    )
    return {"Status" : "Success", "Results" : len(result), "Pedidos" : result}
@router.delete("/pedidos")
async def excluir_registros_teste(db: Session = Depends(get_db)):
    registro_para_excluir = db.query(models.StatusPedido).filter_by(id = "azumas").first()
    if registro_para_excluir:
        db.delete(registro_para_excluir)
        db.commit()
        return {"Status" : "Success"}
    else:
        raise HTTPException(status_code=404, detail = "Registro teste não encontrado")
