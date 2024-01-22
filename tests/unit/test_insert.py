from fastapi.testclient import TestClient
import os

os.environ["TESTING"] = "True"

from app.main import app

client = TestClient(app)

def test_noPreviousOrder_insertOrder_orderInserted():    
    sample_payload = {
        "id" : "azumas",
        "numeropedido" : "12345678",
        "timestamp" : "2023-03-17T00:04:32"
    }
    response = client.post("/kitchen/criar_pedido", json=sample_payload)
    assert response.status_code == 201
    assert response.json() == {
        "message": "Pedido criado com sucesso"
    }

def test_hasPreviousOrder_insertOrder_duplicatedOrder():    
    sample_payload = {
        "id" : "azumas",
        "numeropedido" : "12345678",
        "timestamp" : "2023-03-17T00:04:32"
    }
    response1 = client.post("/kitchen/criar_pedido", json=sample_payload)
    response2 = client.post("/kitchen/criar_pedido", json=sample_payload)

    assert response2.status_code == 400

del os.environ["TESTING"]