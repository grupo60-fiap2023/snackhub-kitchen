# from fastapi.testclient import TestClient
# from main import app, engine, pedidos

# from sqlalchemy.sql import func
# from sqlalchemy import create_engine, Table, MetaData, select, update, insert, Column, String, Float, Integer, DateTime

# client = TestClient(app)
# dateNow = func.now()

# def noPreviousOrder_insertOrder_orderInserted():
#     sample_payload = {
#         "id" : "azumas",
#         "numeropedido" : "12345678",
#         "timestamp" : dateNow
#     }
#     response = client.post("/criar_pedido", json=sample_payload)
#     assert response.status_code == 201
#     assert response.json() == {
#         "message": "Pedido criado com sucesso"
#     }

#     #verificando se o registro foi inserido
#     with engine.connect() as connection:
#         result = connection.execute(select(pedidos).where(pedidos.columns.id == "azumas")).fetchone()
#         assert result is not None
#         assert result[1] == 12345678
#         assert result[2] == dateNow
#         assert result[4] == 1 

# def hasPreviousOrder_insertOrder_duplicatedOrder():
#     sample_payload = {
#         "id" : "azumas",
#         "numeropedido" : "12345678",
#         "timestamp" : dateNow
#     }
#     response1 = client.post("/criar_pedido", json=sample_payload)
#     response2 = client.post("/criar_pedido", json=sample_payload)

#     assert response2.status_code == 400

