from app.models import Player

def test_player_creation():
    p = Player(id="1", nome="Pedro", gols=10, assistencias=5, minutos_jogados=90)
    assert p.id == "1"
    assert p.nome == "Pedro"
    assert p.gols == 10
    assert p.assistencias == 5
    assert p.minutos_jogados == 90
