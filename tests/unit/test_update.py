from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#Em preparação
def test_orderAwaiting_statusToPreparing_orderPreparing():
    response = client.put('/kitchen/statusempreparacao/azumas')
    assert response.status_code == 200
    assert response.json() == {
        "message" : "Pedido 'azumas' atualizado com sucesso"
    }

def test_orderStatusPreparing_statusToPreparing_orderNotUpdated():
    response = client.put('/kitchen/statusempreparacao/azumas')
    assert response.status_code == 400
    assert response.json() == {
            "detail": "Pedido 'azumas' não pode mudar para o status 2"
    }

def test_noPreviousOrder_statusToPreparing_orderNotFound():
    response = client.put('/kitchen/statusempreparacao/nonexistent')
    assert response.status_code == 404
    assert response.json() == {
            "detail": "Pedido numero 'nonexistent' não encontrado"
    }

#Pronto para entrega
def test_orderPreparing_statusToReadyToDeliver_orderReadyToDeliver():
    response = client.put('/kitchen/statuspronto/azumas')
    assert response.status_code == 200
    assert response.json() == {
        "message" : "Pedido 'azumas' atualizado com sucesso"
    }

def test_orderStatusReadyToDeliver_statusToReadyToDeliver_orderNotUpdated():
    response = client.put('/kitchen/statuspronto/azumas')
    assert response.status_code == 400
    assert response.json() == {
            "detail": "Pedido 'azumas' não pode mudar para o status 3"
    }

def test_noPreviousOrder_statusToReadyToDeliver_orderNotFound():
    response = client.put('/kitchen/statuspronto/nonexistent')
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Pedido numero 'nonexistent' não encontrado"
    }
    
#Finalizado
def test_orderReadyToDeliver_statusToDone_orderDone():
    response = client.put('/kitchen/statusfinalizado/azumas')
    assert response.status_code == 200
    assert response.json() == {
        "message" : "Pedido 'azumas' atualizado com sucesso"
    }

def test_orderStatusDone_statusToDone_orderNotUpdated():
    response = client.put('/kitchen/statusfinalizado/azumas')
    assert response.status_code == 400
    assert response.json() == {
            "detail": "Pedido 'azumas' não pode mudar para o status 4"
    }

def test_noPreviousOrder_statusToDone_orderNotFound():
    response = client.put('/kitchen/statusfinalizado/nonexistent')
    assert response.status_code == 404
    assert response.json() == {
            "detail": "Pedido numero 'nonexistent' não encontrado"
    }