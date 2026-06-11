from app.models import Player

def test_player_creation():
    p = Player(id="1", nome="Pedro", gols=10, assistencias=5, minutos_jogados=90)
    assert p.id == "1"
    assert p.gols == 10