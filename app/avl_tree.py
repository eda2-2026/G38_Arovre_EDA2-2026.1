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
