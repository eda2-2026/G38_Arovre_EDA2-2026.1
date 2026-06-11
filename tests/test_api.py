from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_ranking():
    response = client.get("/api/ranking?criterio=gols")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_player():
    data = {"id": "999", "nome": "Novo", "gols": 1, "assistencias": 1, "minutos_jogados": 10}
    response = client.post("/api/players", json=data)
    assert response.status_code == 200
