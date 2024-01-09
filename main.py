import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Table, MetaData, select, update, insert, Column, String, Float, Integer, DateTime
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func

# Configuração do SQLAlchemy
DATABASE_URL = "mysql+mysqlconnector://root:123456@snackhub-mysql-db-kitchen:3306/pedidos"
#DATABASE_URL = "mysql+mysqlconnector://root:123456@localhost:3307/pedidos"
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Criando tabela se não existir
pedidos = Table(
   'LogStatusPedido', metadata, 
   Column('id', String(255), primary_key=True),
   Column('numeropedido', Integer),
   Column('timestamp', DateTime(timezone = True), server_default=func.now()), 
   Column('updatedAt', DateTime(timezone = True), onupdate=func.now()),
   Column('status', Integer)
)
metadata.create_all(engine)

# Gerenciamento de sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()

class CriarPedido(BaseModel):
    id: str
    numeropedido: int

class StatusPedido(BaseModel):
    id: str
    numeropedido: int
    status : int

@app.post("/criar_pedido")
async def criar_pedido(pedido: CriarPedido):
    # Criar uma nova sessão
    session = SessionLocal()
    try:
        insert_query = insert(pedidos).values(
            id=pedido.id,
            numeropedido = pedido.numeropedido,
            timestamp = func.now(),
            status=1)
        result = session.execute(insert_query)
        # Confirmar as mudanças
        session.commit()
        if result.rowcount == 0:
            raise HTTPException(status_code=400, detail="Erro ao registrar pedido")
        return {"message": "Pedido criado com sucesso"}
    except Exception as e:
        # Reverter as mudanças em caso de erro
        session.rollback()
        raise HTTPException(status_code=400, detail=f"Erro ao registrar pedido: {e}")
    finally:
        # Fechar a sessão
        session.close()

@app.put("/statusempreparacao/{idPedido}")
async def atualizar_status_em_preparacao(idPedido : str):
    return AtualizarStatus(idPedido, 2)

@app.put("/statuspronto/{idPedido}")
async def atualizar_status_pronto(idPedido : str):
    return AtualizarStatus(idPedido, 3)

@app.put("/statusfinalizado/{idPedido}")
async def atualizar_status_finalizado(idPedido : str):
    return AtualizarStatus(idPedido, 4)

def AtualizarStatus(idPedido: int, status : int):
    query = select(pedidos).where(pedidos.columns.id ==idPedido)
    with engine.connect() as connection:
        try:
            result = connection.execute(query).fetchone()
            if result is None:
                raise HTTPException(status_code=404, detail="Produto não encontrado")
            # Mapear valores para nomes de colunas
            column_names = [column.name for column in pedidos.c]
            result_dict = dict(zip(column_names, result))
            pedidoSelecionado = StatusPedido(**result_dict)  # Passar o dicionário para Produto

            if pedidoSelecionado.status + 1 != status:
                raise HTTPException(status_code=400, detail="Pedido {} não pode mudar para o status {}".format(pedidoSelecionado.numeropedido, status))
            session = SessionLocal()
            try:
                update_query = update(pedidos).where(pedidos.columns.id == idPedido).values(
                    status=status
                )
                result = session.execute(update_query)
                #Commitando as mudanças
                session.commit()
                if result.rowcount ==0:
                    raise HTTPException(status_code=400, detail="Erro ao atualizar status do produto.")
                return {"Message": "Atualização de status criado com sucesso"}
            except Exception as e:
                session.rollback()
                raise HTTPException(status_code=400, detail=f"Erro ao atualizar status do produto: {e}")
            finally:
                session.close()


        except NoResultFound:
            raise HTTPException(status_code=404, detail="Produto não encontrado")

    

@app.get("/pedidos/{status}")
async def obter_pedidos_por_status(status : int):
    query = select(pedidos).where(pedidos.columns.status == status)
    with engine.connect() as connection:
        try:
            column_names = [column.name for column in pedidos.c]
            result = connection.execute(query).fetchall()
            
            list = []
            for i in result:
                d = {'id' : i[0],
                     'numeropedido' : i[1],
                     'timestamp' : i[2],
                     'updatedAt' : i[3],
                     'status' : i[4]}
                list.append(d)
            
            return {"data": list}
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Nenhum pedido com esse status foi encontrado.")
        except:
            raise Exception("Erro desconhecido")