import heapq # Імпорт бібліотеки для роботи з купою (heap)  
from typing import List, Tuple # Імпорт типів для анотації функцій 

def min_merge_cost(lengths: List[int]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Обчислює мінімальні загальні витрати на об'єднання кабелів.
    Повертає (total_cost, steps), де steps — список кроків (a, b, a + b).
    """
    if not lengths:       # Якщо список порожній 
        return 0, []      # нічого з'єднувати 
    if len(lengths) == 1: # Якщо лише один кабель 
        return 0, []      # нічого з'єднувати

    heap = list(lengths) # Створення купи з довжин кабелів 
    heapq.heapify(heap)  # Перетворення списку в купу 

    total = 0        
    steps: List[Tuple[int, int, int]] = [] # Список кроків об'єднання 

    while len(heap) > 1:          # Поки в купі більше одного елемента 
        a = heapq.heappop(heap)   # Витягуємо найкоротший кабель
        b = heapq.heappop(heap)   # Витягуємо другий найкоротній кабель
        sum = a + b               # Вартість об'єднання двох кабелів
        total += sum              # Додаємо вартість до загальної суми
        steps.append((a, b, sum)) # Записуємо крок об'єднання 
        heapq.heappush(heap, sum) # Повертаємо новий кабель в купу 

    return total, steps           # Повертаємо загальні витрати та кроки об'єднання

# Приклад використання
if __name__ == "__main__":
    lengths = [8, 4, 6, 12, 10]                # довжини кабелів для об'єднання 
    total, steps = min_merge_cost(lengths)     # обчислення мінімальних витрат 
    print("Довжини кабелів:", lengths)         # вхідні дані 
    print("Кроки об'єднання (a, b -> a + b):") # виведення кроків 
    for a, b, sum in steps:                    # виведення кожного кроку 
        print(f"  {a} + {b} -> {sum}")         # форматований вивід 
    print("Мінімальні загальні витрати:", total)