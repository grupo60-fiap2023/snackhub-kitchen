from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

AZUMAS_SUCCESS = "Pedido 'azumas' atualizado com sucesso"
NONEXISTENT_NOT_FOUND = "Pedido numero 'nonexistent' não encontrado"
#Em preparação
def test_orderawaiting_statustopreparing_orderpreparing():
    response = client.put('/kitchen/statusempreparacao/azumas')
    assert response.status_code == 200
    assert response.json() == {
        "message" : AZUMAS_SUCCESS
    }

def test_orderstatuspreparing_statustopreparing_ordernotupdated():
    response = client.put('/kitchen/statusempreparacao/azumas')
    assert response.status_code == 400
    assert response.json() == {
            "detail": "Pedido 'azumas' não pode mudar para o status 2"
    }

def test_nopreviousorder_statustopreparing_ordernotfound():
    response = client.put('/kitchen/statusempreparacao/nonexistent')
    assert response.status_code == 404
    assert response.json() == {
            "detail": NONEXISTENT_NOT_FOUND
    }
    
#Finalizado
def test_orderreadytodeliver_statustodone_orderdone():
    response = client.put('/kitchen/statusfinalizado/azumas')
    assert response.status_code == 200
    assert response.json() == {
        "message" : AZUMAS_SUCCESS
    }

def test_orderstatusdone_statustodone_ordernotupdated():
    response = client.put('/kitchen/statusfinalizado/azumas')
    assert response.status_code == 400
    assert response.json() == {
            "detail": "Pedido 'azumas' não pode mudar para o status 4"
    }

def test_nopreviousorder_statustodone_ordernotfound():
    response = client.put('/kitchen/statusfinalizado/nonexistent')
    assert response.status_code == 404
    assert response.json() == {
            "detail": NONEXISTENT_NOT_FOUND
    }