from pydantic import BaseModel

class Player(BaseModel):
    id: str
    nome: str
    gols: int
    assistencias: int
    minutos_jogados: int
