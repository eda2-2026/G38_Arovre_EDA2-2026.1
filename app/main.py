# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.models import Player
from app.avl_tree import AVLTree
import os
import json

app = FastAPI()

# Caminho para o arquivo de dados
DATA_FILE = os.path.join(os.path.dirname(__file__), "players.json")

def load_players():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Player(**p) for p in data]
    return []

def save_players(players):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([p.model_dump() for p in players], f, ensure_ascii=False, indent=4)

# Memória da aplicação
players_db = load_players()
tree = AVLTree()
current_criterio = "gols"

def rebuild_tree_instance(criterio, players):
    new_tree = AVLTree()
    for p in players:
        key = getattr(p, criterio)
        new_tree.insert(key, p)
    return new_tree

# Inicialização
tree = rebuild_tree_instance(current_criterio, players_db)

@app.get("/api/ranking")
def get_ranking(criterio: str = "gols"):
    global current_criterio, tree
    if criterio not in ["gols", "assistencias", "minutos_jogados"]:
        raise HTTPException(status_code=400, detail="Critério inválido")
    
    if criterio != current_criterio:
        new_tree = rebuild_tree_instance(criterio, players_db)
        tree = new_tree # Swap atômico
        current_criterio = criterio
        
    ranking = tree.in_order_reverse()
    return ranking

@app.post("/api/players")
def add_player(player: Player):
    # Verificar se ID já existe
    if any(p.id == player.id for p in players_db):
        raise HTTPException(status_code=400, detail="ID já existe")
        
    players_db.append(player)
    save_players(players_db)
    
    key = getattr(player, current_criterio)
    tree.insert(key, player)
    return {"message": "Jogador adicionado com sucesso"}

@app.delete("/api/players/{id}")
def delete_player(id: str):
    global players_db
    player_to_delete = next((p for p in players_db if p.id == id), None)
    if not player_to_delete:
        raise HTTPException(status_code=404, detail="Jogador não encontrado")
    
    # Remover do banco em memória
    players_db = [p for p in players_db if p.id != id]
    save_players(players_db)
    
    # Remover da árvore
    key = getattr(player_to_delete, current_criterio)
    tree.delete(key, id)
    
    return {"message": "Jogador removido com sucesso"}

# Monte os arquivos estáticos após definir a API se a pasta existir
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
