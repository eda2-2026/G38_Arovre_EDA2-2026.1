# app/avl_tree.py
class AVLNode:
    def __init__(self, key):
        self.key = key
        self.values = []
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        self.root = None

    def get_height(self, node):
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def right_rotate(self, y):
        x = y.left
        t2 = x.right
        x.right = y
        y.left = t2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def left_rotate(self, x):
        y = x.right
        t2 = y.left
        y.left = x
        x.right = t2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, key, player):
        self.root = self._insert(self.root, key, player)

    def _insert(self, root, key, player):
        if not root:
            node = AVLNode(key)
            node.values.append(player)
            return node
        
        if key < root.key:
            root.left = self._insert(root.left, key, player)
        elif key > root.key:
            root.right = self._insert(root.right, key, player)
        else:
            root.values.append(player)
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)
        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)
        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def in_order_reverse(self):
        return self._in_order_reverse(self.root)

    def _in_order_reverse(self, root):
        result = []
        if root:
            result.extend(self._in_order_reverse(root.right))
            result.extend(root.values)
            result.extend(self._in_order_reverse(root.left))
        return result

    def get_min_value_node(self, node):
        if node is None or node.left is None:
            return node
        return self.get_min_value_node(node.left)

    def delete(self, key, player_id):
        self.root = self._delete(self.root, key, player_id)

    def _delete(self, root, key, player_id):
        if not root:
            return root
            
        if key < root.key:
            root.left = self._delete(root.left, key, player_id)
        elif key > root.key:
            root.right = self._delete(root.right, key, player_id)
        else:
            # Encontrou o nó. Remover o jogador da lista
            root.values = [p for p in root.values if p.id != player_id]
            if len(root.values) > 0:
                # Se ainda tem jogadores com essa chave, não remove o nó
                return root
                
            # Nó com apenas um filho ou nenhum
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp
                
            # Nó com dois filhos
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.values = temp.values
            root.right = self._delete_node(root.right, temp.key)

        if root is None:
            return root

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def _delete_node(self, root, key):
        if not root:
            return root
        if key < root.key:
            root.left = self._delete_node(root.left, key)
        elif key > root.key:
            root.right = self._delete_node(root.right, key)
        else:
            if root.left is None:
                return root.right
            elif root.right is None:
                return root.left
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.values = temp.values
            root.right = self._delete_node(root.right, temp.key)
            
        if root is None:
            return root
            
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)
        
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)
        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root
