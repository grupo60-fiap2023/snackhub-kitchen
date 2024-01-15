from fastapi.testclient import TestClient
from app.main import app

from sqlalchemy.sql import func
from sqlalchemy import select

client = TestClient(app)

def noPreviousOrder_insertOrder_orderInserted():
    sample_payload = {
        "id" : "azumas",
        "numeropedido" : "12345678",
        "timestamp" : "2023-03-17T00:04:32"
    }
    response = client.post("/criar_pedido", json=sample_payload)
    assert response.status_code == 201
    assert response.json() == {
        "message": "Pedido criado com sucesso"
    }

def hasPreviousOrder_insertOrder_duplicatedOrder():
    sample_payload = {
        "id" : "azumas",
        "numeropedido" : "12345678",
        "timestamp" : "2023-03-17T00:04:32"
    }
    response1 = client.post("/criar_pedido", json=sample_payload)
    response2 = client.post("/criar_pedido", json=sample_payload)

    assert response2.status_code == 400

