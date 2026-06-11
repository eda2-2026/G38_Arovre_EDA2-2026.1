from fastapi.testclient import TestClient
from app.main import app
import json
import os

client = TestClient(app)

def test_get_ranking_order():
    # Verify ranking by goals (default)
    response = client.get("/api/ranking?criterio=gols")
    assert response.status_code == 200
    ranking = response.json()
    assert len(ranking) >= 2
    # Check descending order
    for i in range(len(ranking) - 1):
        assert ranking[i]["gols"] >= ranking[i+1]["gols"]

def test_switch_criteria():
    # Verify ranking by assists
    response = client.get("/api/ranking?criterio=assistencias")
    assert response.status_code == 200
    ranking = response.json()
    # Check descending order by assists
    for i in range(len(ranking) - 1):
        assert ranking[i]["assistencias"] >= ranking[i+1]["assistencias"]
        
    # Verify ranking by minutes_jogados
    response = client.get("/api/ranking?criterio=minutos_jogados")
    assert response.status_code == 200
    ranking = response.json()
    for i in range(len(ranking) - 1):
        assert ranking[i]["minutos_jogados"] >= ranking[i+1]["minutos_jogados"]

def test_add_and_delete_player():
    player_id = "test_999"
    new_player = {
        "id": player_id,
        "nome": "Test Player",
        "gols": 999,
        "assistencias": 999,
        "minutos_jogados": 999
    }
    
    # 1. Add player
    response = client.post("/api/players", json=new_player)
    assert response.status_code == 200
    
    # 2. Verify player is at the top of ranking
    response = client.get("/api/ranking?criterio=gols")
    ranking = response.json()
    assert ranking[0]["id"] == player_id
    assert ranking[0]["gols"] == 999
    
    # 3. Delete player
    response = client.delete(f"/api/players/{player_id}")
    assert response.status_code == 200
    
    # 4. Verify player is gone
    response = client.get("/api/ranking?criterio=gols")
    ranking = response.json()
    assert all(p["id"] != player_id for p in ranking)

def test_invalid_criteria():
    response = client.get("/api/ranking?criterio=invalid")
    assert response.status_code == 400
    assert response.json()["detail"] == "Critério inválido"

def test_delete_non_existent():
    response = client.delete("/api/players/non_existent_id")
    assert response.status_code == 404
    assert response.json()["detail"] == "Jogador não encontrado"

def test_add_duplicate_id():
    # First, get an existing ID
    response = client.get("/api/ranking")
    existing_player = response.json()[0]
    
    duplicate_player = {
        "id": existing_player["id"],
        "nome": "Duplicate",
        "gols": 0,
        "assistencias": 0,
        "minutos_jogados": 0
    }
    response = client.post("/api/players", json=duplicate_player)
    assert response.status_code == 400
    assert response.json()["detail"] == "ID já existe"
