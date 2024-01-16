from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_findStatusDone_foundOneRegister():
    response = client.get('kitchen/pedidos/4')
    assert response.status_code == 200
    
    
def test_findStatusPreparing_foundNoRegister():
    response = client.get('kitchen/pedidos/4')
    assert response.status_code == 200
    assert response.json() == {
        "Status": "Success",
        "Results": 0,
        "Pedidos": []
    }