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

# Aвтоматичне балансування AVL дерева 
def get_height(n: "Node | None") -> int:
    return n.height if n else 0

def update_height(n: "Node") -> None:
    n.height = 1 + max(get_height(n.left), get_height(n.right))

def get_balance(n: "Node | None") -> int:
    return (get_height(n.left) - get_height(n.right)) if n else 0

def right_rotate(y: "Node") -> "Node":
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    update_height(y)
    update_height(x)
    return x

def left_rotate(x: "Node") -> "Node":
    y = x.right
    T2 = y.left
    y.left = x
    x.right = T2
    update_height(x)
    update_height(y)
    return y

def insert(root: "Node | None", key: int) -> "Node":
    if root is None:
        return Node(key)
    if key < root.val:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)

    update_height(root)
    balance = get_balance(root)

    # LL
    # баланс > 1 означає, що ліве піддерево вищє за праве більше ніж на 1 висоту 
    if balance > 1 and key < root.left.val:
        return right_rotate(root)
    # RR
    # баланс < -1 означає, що праве піддерево вищє за ліве більше ніж на 1 висоту 
    if balance < -1 and key > root.right.val:
        return left_rotate(root)
    # LR
    # баланс > 1 означає, що ліве піддерево вищє за праве більше ніж на 1 висоту 
    if balance > 1 and key > root.left.val:
        root.left = left_rotate(root.left)
        return right_rotate(root)
    # RL
    # баланс < -1 означає, що праве піддерево вищє за ліве більше ніж на 1 висоту 
    if balance < -1 and key < root.right.val:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root

# Cума всіх значень в AVL дереві 
def sum_values(root: "Node | None") -> int:
    """Рекурсивна сума всіх ключів."""
    if root is None:
        return 0
    return root.val + sum_values(root.left) + sum_values(root.right)

def sum_values_iter(root: "Node | None") -> int:
    """Ітеративна сума (без рекурсії) через стек."""
    if root is None:
        return 0
    total = 0
    stack = [root]
    while stack:
        node = stack.pop()
        total += node.val
        if node.left: stack.append(node.left)
        if node.right: stack.append(node.right)
    return total

# Візуалізація AVL дерева 
def compute_positions(root: "Node | None"):
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

def tree_size(node: "Node | None"):
    return 0 if node is None else 1 + tree_size(node.left) + tree_size(node.right)

def tree_height(node: "Node | None"):
    return -1 if node is None else 1 + max(tree_height(node.left), tree_height(node.right))

def draw_tree(root: "Node | None"):
    if not root:
        print("Дерево порожнє")
        return

    pos = compute_positions(root)
    n = tree_size(root)
    h = tree_height(root)

    fig_w = max(6, n * 0.7)
    fig_h = max(4, (h + 1) * 1.2)
    plt.figure(figsize=(fig_w, fig_h))

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
    plt.scatter(xs, ys, s=base_size, zorder=3,
                edgecolors="none", facecolors="#8ecae6")

    # Підписи вузлів 
    fs = 12 if n < 15 else 10 if n < 25 else 8
    for node, (x, y) in pos.items():
        plt.text(x, y, str(node.val), ha="center", va="center", fontsize=fs, zorder=4)

    pad_x = max(0.5, n * 0.05)
    pad_y = max(0.3, (h + 1) * 0.15)
    plt.xlim(min(xs) - pad_x, max(xs) + pad_x)
    plt.ylim(min(ys) - pad_y, max(ys) + pad_y)
    plt.axis("off")
    plt.show()

# Тестування AVL дерева та суми значень 
if __name__ == "__main__":
    values = random.sample(range(1, 50), 11)
    print("\nЗгенеровані:", values)

    root = None                # створення AVL дерева 
    for v in values:           # вставка кожного числа в AVL дерево
        root = insert(root, v) # вставка з балансуванням 

    print("\nAVL дерево:")
    print(root)

    print("Сума всіх значень (рекурсивно):", sum_values(root))
    print("Сума всіх значень (ітеративно):", sum_values_iter(root))
    print("\n")
    
    draw_tree(root)