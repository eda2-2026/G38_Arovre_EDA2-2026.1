# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from app.models import Player
from app.avl_tree import AVLTree
import os

app = FastAPI()

# Memória da aplicação
players_db = [
    Player(id="1", nome="Neymar", gols=100, assistencias=50, minutos_jogados=3000),
    Player(id="2", nome="Vini Jr", gols=80, assistencias=60, minutos_jogados=2500)
]
tree = AVLTree()
current_criterio = "gols"

def rebuild_tree(criterio):
    tree.root = None # Reset root directly or create new tree
    for p in players_db:
        key = getattr(p, criterio)
        tree.insert(key, p)

rebuild_tree(current_criterio)

@app.get("/api/ranking")
def get_ranking(criterio: str = "gols"):
    global current_criterio
    if criterio not in ["gols", "assistencias", "minutos_jogados"]:
        raise HTTPException(status_code=400, detail="Critério inválido")
    
    if criterio != current_criterio:
        current_criterio = criterio
        rebuild_tree(criterio)
        
    ranking = tree.in_order_reverse()
    return ranking

@app.post("/api/players")
def add_player(player: Player):
    players_db.append(player)
    key = getattr(player, current_criterio)
    tree.insert(key, player)
    return {"message": "Jogador adicionado com sucesso"}

# Monte os arquivos estáticos após definir a API se a pasta existir
if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
