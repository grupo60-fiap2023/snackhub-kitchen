from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_findstatusdone_foundoneregister():
    response = client.get('kitchen/pedidos/4')
    assert response.status_code == 200