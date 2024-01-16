from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_findStatusDone_foundOneRegister():
    response = client.get('kitchen/pedidos/4')
    assert response.status_code == 200