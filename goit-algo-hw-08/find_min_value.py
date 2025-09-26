import random # для генерації випадкових чисел та тестування дерева 
import matplotlib.pyplot as plt # для візуалізації дерева 

# Вузол AVL дерева 
class Node: 
    def __init__(self, key):
        self.left = None
        self.right = None
        self.val = key
        self.height = 1

    # Для зручного виведення дерева в консоль 
    def __str__(self, level=0, prefix="\nRoot: "):
        ret = "\t" * level + prefix + str(self.val) + "\n"
        if self.left:
            ret += self.left.__str__(level + 1, "L--- ")
        if self.right:
            ret += self.right.__str__(level + 1, "R--- ")
        return ret

# Отримання висоти вузла 
def get_height(n: Node | None) -> int:
    return n.height if n else 0

# Оновлення висоти вузла 
def update_height(n: Node) -> None:
    n.height = 1 + max(get_height(n.left), get_height(n.right))

# Баланс фактор вузла 
def get_balance(n: Node | None) -> int:
    return (get_height(n.left) - get_height(n.right)) if n else 0

# Праве обертання вузла
def right_rotate(y: Node) -> Node: # праве обертання вузла 
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    update_height(y)
    update_height(x)
    return x

# Ліве обертання вузла
def left_rotate(x: Node) -> Node:
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    update_height(x)
    update_height(y)
    return y

# Вставка вузла з балансуванням в AVL дерево
def insert(root: Node | None, key: int) -> Node: 
    if root is None:
        return Node(key)
    if key < root.val:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    # Оновлення висоти вузла
    update_height(root) 
    balance = get_balance(root)

    # LL
    # баланс > 1 означає, що ліве піддерево вищє за праве
    if balance > 1 and key < root.left.val:
        return right_rotate(root)
    # RR
    # баланс < -1 означає, що праве піддерево вищє за ліве 
    if balance < -1 and key > root.right.val:
        return left_rotate(root)
    # LR
    # баланс > 1 означає, що ліве піддерево вищє за праве
    # а ключ > root.left.val означає, що ключ вставляється в праве піддерево лівого піддерева 
    if balance > 1 and key > root.left.val:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    # RL
    # баланс < -1 означає, що праве піддерево вищє за ліве   
    # а ключ < root.right.val означає, що ключ вставляється в ліве піддерево правого піддерева 
    if balance < -1 and key < root.right.val:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root

# Знаходження мінімального значення в AVL дереві 
def find_min(root: Node | None):
    if root is None:
        return None
    cur = root
    while cur.left:
        cur = cur.left
    return cur.val

# Візуалізація AVL дерева з підсвіткою мінімального значення 
def compute_positions(root):
    pos = {}
    x_counter = 0
    def dfs(node, depth):
        nonlocal x_counter
        if not node: return
        dfs(node.left, depth + 1)
        pos[node] = (x_counter, -depth)
        x_counter += 1
        dfs(node.right, depth + 1)
    dfs(root, 0)
    return pos

# Розмір та висота дерева
def tree_size(node):
    return 0 if node is None else 1 + tree_size(node.left) + tree_size(node.right)

def tree_height(node):
    return -1 if node is None else 1 + max(tree_height(node.left), tree_height(node.right))

def draw_tree(root, highlight_min=True):
    if not root:
        print("Дерево порожнє")
        return

    pos = compute_positions(root) # позиції вузлів для візуалізації 
    n = tree_size(root)           # кількість вузлів 
    h = tree_height(root)         # висота дерева 

    fig_w = max(6, n * 0.7)            # ширина фігури 
    fig_h = max(4, (h + 1) * 1.2)      # висота фігури 
    plt.figure(figsize=(fig_w, fig_h)) # створення фігури   

    # Ребра дерева
    def draw_edges(node):
        if not node: return
        x1, y1 = pos[node]
        if node.left:
            x2, y2 = pos[node.left]
            plt.plot([x1, x2], [y1, y2], color="#444")
            draw_edges(node.left)
        if node.right:
            x2, y2 = pos[node.right]
            plt.plot([x1, x2], [y1, y2], color="#444")
            draw_edges(node.right)
    draw_edges(root)

    # Вузли дерева
    xs = [xy[0] for xy in pos.values()]
    ys = [xy[1] for xy in pos.values()]
    base_size = max(800, int(5000 / max(1, n)))
    plt.scatter(xs, ys, s=base_size, zorder=3, edgecolors="None", linewidths=1.5,
                facecolors="#8ecae6")

    # Підписи вузлів
    fs = 12 if n < 15 else 10 if n < 25 else 8
    for node, (x, y) in pos.items():
        plt.text(x, y, str(node.val), ha="center", va="center", fontsize=fs, zorder=4)

    # Підсвітка мінімального значення 
    if highlight_min:
        m = find_min(root)
        min_node = next(nd for nd in pos if nd.val == m)
        x, y = pos[min_node]
        plt.scatter([x], [y], s=base_size * 1.2, zorder=5,
                    edgecolors="red", linewidths=2, facecolors="none")

    pad_x = max(0.5, n * 0.05)                   # відступ по x
    pad_y = max(0.3, (h + 1) * 0.15)             # відступ по y 
    plt.xlim(min(xs) - pad_x, max(xs) + pad_x)   # межі по x 
    plt.ylim(min(ys) - pad_y, max(ys) + pad_y)   # межі по y 
    plt.axis("off")                              # вимкнення осей 
    plt.show()                                   # показ фігури 

# Тестування AVL дерева та пошук мінімального значення 
values = random.sample(range(1, 50), 11) # унікальні випадкові числа від 1 до 49 
print("\nЗгенеровані:", values)          # виведення згенерованих чисел 

root = None                # корінь AVL дерева 
for v in values:           # вставка кожного числа в AVL дерево 
    root = insert(root, v) # вставка з балансуванням 

print("\nAVL дерево:")
print(root)
print("Мінімальне значення:", find_min(root))
print("\n")

draw_tree(root, highlight_min=True)