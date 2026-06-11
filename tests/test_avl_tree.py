# tests/test_avl_tree.py
from app.avl_tree import AVLTree, AVLNode
from app.models import Player

def test_avl_insert_and_in_order_reverse():
    tree = AVLTree()
    
    p1 = Player(id="1", nome="A", gols=5, assistencias=0, minutos_jogados=0)
    p2 = Player(id="2", nome="B", gols=10, assistencias=0, minutos_jogados=0)
    p3 = Player(id="3", nome="C", gols=5, assistencias=0, minutos_jogados=0)
    
    # Inserindo por gols
    tree.insert(p1.gols, p1)
    tree.insert(p2.gols, p2)
    tree.insert(p3.gols, p3)
    
    result = tree.in_order_reverse()
    
    assert len(result) == 3
    assert result[0].id == "2" # 10 gols
    assert result[1].id in ["1", "3"] # 5 gols
    assert result[2].id in ["1", "3"]

def test_avl_left_left_rotation():
    tree = AVLTree()
    # Inserting 3, 2, 1 will trigger a Right Rotation on 3 (which fixes a Left-Left heavy situation)
    p1 = Player(id="1", nome="A", gols=3, assistencias=0, minutos_jogados=0)
    p2 = Player(id="2", nome="B", gols=2, assistencias=0, minutos_jogados=0)
    p3 = Player(id="3", nome="C", gols=1, assistencias=0, minutos_jogados=0)

    tree.insert(p1.gols, p1)
    tree.insert(p2.gols, p2)
    tree.insert(p3.gols, p3)

    # After rotation, root should be 2, left should be 1, right should be 3
    assert tree.root.key == 2
    assert tree.root.left.key == 1
    assert tree.root.right.key == 3

def test_avl_right_right_rotation():
    tree = AVLTree()
    # Inserting 1, 2, 3 will trigger a Left Rotation on 1 (which fixes a Right-Right heavy situation)
    p1 = Player(id="1", nome="A", gols=1, assistencias=0, minutos_jogados=0)
    p2 = Player(id="2", nome="B", gols=2, assistencias=0, minutos_jogados=0)
    p3 = Player(id="3", nome="C", gols=3, assistencias=0, minutos_jogados=0)

    tree.insert(p1.gols, p1)
    tree.insert(p2.gols, p2)
    tree.insert(p3.gols, p3)

    # After rotation, root should be 2, left should be 1, right should be 3
    assert tree.root.key == 2
    assert tree.root.left.key == 1
    assert tree.root.right.key == 3

def test_avl_left_right_rotation():
    tree = AVLTree()
    # Inserting 3, 1, 2 will trigger a Left-Right Rotation
    p1 = Player(id="1", nome="A", gols=3, assistencias=0, minutos_jogados=0)
    p2 = Player(id="2", nome="B", gols=1, assistencias=0, minutos_jogados=0)
    p3 = Player(id="3", nome="C", gols=2, assistencias=0, minutos_jogados=0)

    tree.insert(p1.gols, p1)
    tree.insert(p2.gols, p2)
    tree.insert(p3.gols, p3)

    # After rotation, root should be 2, left should be 1, right should be 3
    assert tree.root.key == 2
    assert tree.root.left.key == 1
    assert tree.root.right.key == 3

def test_avl_right_left_rotation():
    tree = AVLTree()
    # Inserting 1, 3, 2 will trigger a Right-Left Rotation
    p1 = Player(id="1", nome="A", gols=1, assistencias=0, minutos_jogados=0)
    p2 = Player(id="2", nome="B", gols=3, assistencias=0, minutos_jogados=0)
    p3 = Player(id="3", nome="C", gols=2, assistencias=0, minutos_jogados=0)

    tree.insert(p1.gols, p1)
    tree.insert(p2.gols, p2)
    tree.insert(p3.gols, p3)

    # After rotation, root should be 2, left should be 1, right should be 3
    assert tree.root.key == 2
    assert tree.root.left.key == 1
    assert tree.root.right.key == 3
