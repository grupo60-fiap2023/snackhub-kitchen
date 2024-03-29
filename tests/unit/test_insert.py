from fastapi.testclient import TestClient
import os

os.environ["TESTING"] = "True"

from app.main import app

client = TestClient(app)

CREATE_URL = "/kitchen/criar_pedido"

def test_nopreviousorder_insertorder_orderinserted():    
    sample_payload = {
        "id" : "azumas",
        "numeropedido" : "12345678",
        "timestamp" : "2023-03-17T00:04:32"
    }
    response = client.post(CREATE_URL, json=sample_payload)
    assert response.status_code == 201
    assert response.json() == {
        "message": "Pedido criado com sucesso"
    }

def test_haspreviousorder_insertorder_duplicatedorder():    
    sample_payload = {
        "id" : "azumas",
        "numeropedido" : "12345678",
        "timestamp" : "2023-03-17T00:04:32"
    }
    client.post(CREATE_URL, json=sample_payload)
    response2 = client.post(CREATE_URL, json=sample_payload)

    assert response2.status_code == 400

del os.environ["TESTING"]