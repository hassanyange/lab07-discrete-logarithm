"""
test_example.py
Тестирование алгоритма на примере из методички
"""

from main import DiscreteLogarithmSolver

def test_example():
    """Тестирование на примере из методички"""
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА")
    print("="*60)
    
    solver = DiscreteLogarithmSolver()
    
    # Параметры из методички
    p = 107      # простое число
    a = 10       # основание
    b = 64       # значение
    order = 53   # порядок элемента 10 по модулю 107
    
    print(f"Тестовые данные:")
    print(f"  Уравнение: {a}^x ≡ {b} (mod {p})")
    print(f"  Порядок элемента a: {order}")
    print(f"  Ожидаемое решение: x = 20")
    print("-"*60)
    
    # Запуск алгоритма
    x = solver.solve_equation(a, b, p, order)
    
    # Проверка результата
    print("\n" + "="*60)
    print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
    print("="*60)
    
    if x is not None:
        if x == 20:
            print("✓ ТЕСТ ПРОЙДЕН УСПЕШНО!")
            print(f"  Найдено правильное решение: x = {x}")
        else:
            print("✗ ТЕСТ НЕ ПРОЙДЕН")
            print(f"  Найдено решение: x = {x}")
            print(f"  Ожидалось: x = 20")
    else:
        print("✗ ТЕСТ НЕ ПРОЙДЕН")
        print("  Решение не найдено")
    
    print("="*60)


if __name__ == "__main__":
    test_example()