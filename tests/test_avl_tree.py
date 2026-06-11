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
    # Inserting 3, 2, 1 will trigger a Right Rotation on 3
    p1 = Player(id="1", nome="A", gols=3, assistencias=0, minutos_jogados=0)
    p2 = Player(id="2", nome="B", gols=2, assistencias=0, minutos_jogados=0)
    p3 = Player(id="3", nome="C", gols=1, assistencias=0, minutos_jogados=0)

    tree.insert(p1.gols, p1)
    tree.insert(p2.gols, p2)
    tree.insert(p3.gols, p3)

    assert tree.root.key == 2
    assert tree.root.left.key == 1
    assert tree.root.right.key == 3

def test_avl_right_right_rotation():
    tree = AVLTree()
    # Inserting 1, 2, 3 will trigger a Left Rotation on 1
    p1 = Player(id="1", nome="A", gols=1, assistencias=0, minutos_jogados=0)
    p2 = Player(id="2", nome="B", gols=2, assistencias=0, minutos_jogados=0)
    p3 = Player(id="3", nome="C", gols=3, assistencias=0, minutos_jogados=0)

    tree.insert(p1.gols, p1)
    tree.insert(p2.gols, p2)
    tree.insert(p3.gols, p3)

    assert tree.root.key == 2
    assert tree.root.left.key == 1
    assert tree.root.right.key == 3

def test_avl_delete_root():
    tree = AVLTree()
    p1 = Player(id="1", nome="A", gols=5, assistencias=0, minutos_jogados=0)
    tree.insert(p1.gols, p1)
    
    tree.delete(p1.gols, p1.id)
    assert tree.root is None

def test_avl_delete_multi_players():
    tree = AVLTree()
    p1 = Player(id="1", nome="A", gols=5, assistencias=0, minutos_jogados=0)
    p2 = Player(id="2", nome="B", gols=5, assistencias=0, minutos_jogados=0)
    
    tree.insert(p1.gols, p1)
    tree.insert(p2.gols, p2)
    
    # Remove only one player, node should remain
    tree.delete(p1.gols, p1.id)
    assert tree.root is not None
    assert tree.root.key == 5
    assert len(tree.root.values) == 1
    assert tree.root.values[0].id == "2"

def test_avl_delete_node_with_children():
    tree = AVLTree()
    # Create a balanced tree: root=10, left=5, right=15
    players = [
        Player(id="10", nome="A", gols=10, assistencias=0, minutos_jogados=0),
        Player(id="5", nome="B", gols=5, assistencias=0, minutos_jogados=0),
        Player(id="15", nome="C", gols=15, assistencias=0, minutos_jogados=0)
    ]
    for p in players:
        tree.insert(p.gols, p)
        
    # Delete root node (10) which has two children
    tree.delete(10, "10")
    
    assert tree.root.key == 15 # In-order successor should have replaced 10
    assert tree.root.left.key == 5
    assert tree.root.right is None

def test_avl_delete_triggers_rebalance():
    tree = AVLTree()
    # Create a tree that will become unbalanced after deletion
    # Initially:
    #      10
    #     /  \
    #    5    15
    #   /
    #  2
    players = [
        Player(id="10", nome="A", gols=10, assistencias=0, minutos_jogados=0),
        Player(id="5", nome="B", gols=5, assistencias=0, minutos_jogados=0),
        Player(id="15", nome="C", gols=15, assistencias=0, minutos_jogados=0),
        Player(id="2", nome="D", gols=2, assistencias=0, minutos_jogados=0)
    ]
    for p in players:
        tree.insert(p.gols, p)
        
    # Height of 10 is 3, Height of 15 is 1, Height of 5 is 2. Balance = 2-1 = 1 (OK)
    
    # Delete 15. Node 10 becomes unbalanced (Balance = 2-0 = 2)
    # This should trigger a Right Rotation at 10.
    # New root should be 5, with left child 2 and right child 10.
    
    tree.delete(15, "15")
    
    assert tree.root.key == 5
    assert tree.root.left.key == 2
    assert tree.root.right.key == 10
    assert tree.get_height(tree.root) == 2
