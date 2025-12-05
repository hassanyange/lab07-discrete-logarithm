"""
individual_task.py
Решение индивидуального задания
"""

from main import DiscreteLogarithmSolver

def solve_individual_task():
    """Решение индивидуального задания от преподавателя"""
    print("РЕШЕНИЕ ИНДИВИДУАЛЬНОГО ЗАДАНИЯ")
    print("="*60)
    
    solver = DiscreteLogarithmSolver()
    
    # Получение параметров от преподавателя
    print("Введите параметры, полученные от преподавателя:")
    
    try:
        # Пример параметров (заменить на полученные от преподавателя)
        # Обычно преподаватель дает p, a, b
        p = int(input("Простое число p: "))
        a = int(input("Основание a: "))
        b = int(input("Значение b: "))
        
        # Порядок можно не указывать, если неизвестен
        order_input = input("Порядок элемента a (если неизвестен, нажмите Enter): ")
        if order_input.strip():
            order = int(order_input)
        else:
            order = None
            print("Порядок не указан, используется p-1")
        
        print("\n" + "="*60)
        print(f"ПАРАМЕТРЫ ЗАДАНИЯ:")
        print(f"  p = {p}")
        print(f"  a = {a}")
        print(f"  b = {b}")
        if order:
            print(f"  Порядок элемента a: {order}")
        print("="*60)
        
        # Решение уравнения
        x = solver.solve_equation(a, b, p, order)
        
        if x is not None:
            print(f"\n✓ ЗАДАНИЕ РЕШЕНО!")
            print(f"  Ответ: x = {x}")
            
            # Сохранение результата в файл
            with open("result.txt", "w") as f:
                f.write(f"Индивидуальное задание\n")
                f.write(f"Уравнение: {a}^x ≡ {b} (mod {p})\n")
                f.write(f"Решение: x = {x}\n")
                f.write(f"Проверка: {a}^{x} mod {p} = {pow(a, x, p)}\n")
            
            print(f"  Результат сохранен в файл result.txt")
        else:
            print("\n✗ РЕШЕНИЕ НЕ НАЙДЕНО")
            print("  Проверьте правильность введенных параметров")
        
    except ValueError:
        print("Ошибка ввода! Введите целые числа.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    solve_individual_task()