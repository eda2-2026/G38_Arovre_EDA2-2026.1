# tests/test_avl_tree.py
from app.avl_tree import AVLTree, AVLNode
from app.models import Player

def test_avl_insert_and_in_order_reverse():
    tree = AVLTree()
    root = None
    
    p1 = Player(id="1", nome="A", gols=5, assistencias=0, minutos_jogados=0)
    p2 = Player(id="2", nome="B", gols=10, assistencias=0, minutos_jogados=0)
    p3 = Player(id="3", nome="C", gols=5, assistencias=0, minutos_jogados=0)
    
    # Inserindo por gols
    root = tree.insert(root, p1.gols, p1)
    root = tree.insert(root, p2.gols, p2)
    root = tree.insert(root, p3.gols, p3)
    
    result = tree.in_order_reverse(root)
    
    assert len(result) == 3
    assert result[0].id == "2" # 10 gols
    assert result[1].id in ["1", "3"] # 5 gols
    assert result[2].id in ["1", "3"]
