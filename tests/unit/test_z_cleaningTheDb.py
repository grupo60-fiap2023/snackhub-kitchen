from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_z_cleaningthedb():
    response = client.delete('/kitchen/pedidos')
    assert response.status_code == 200  