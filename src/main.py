# ~/work/2023-2024/Криптография/laboratory/lab07/
# ├── main.py              # Main program with algorithm implementation
# ├── test_example.py      # Testing with example from manual
# ├── individual_task.py   # Solve individual assignment
# ├── requirements.txt     # Dependencies (none needed)
# └── README.md           # Documentation

"""
main.py
Основная программа для лабораторной работы №7
Дискретное логарифмирование методом Полларда
"""

import random
import sys

class DiscreteLogarithmSolver:
    """Класс для решения задачи дискретного логарифмирования"""
    
    @staticmethod
    def extended_gcd(a, b):
        """Расширенный алгоритм Евклида"""
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = DiscreteLogarithmSolver.extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    @staticmethod
    def mod_inverse(a, m):
        """Нахождение обратного элемента по модулю m"""
        g, x, _ = DiscreteLogarithmSolver.extended_gcd(a, m)
        if g != 1:
            return None
        return x % m
    
    @staticmethod
    def pollard_rho_discrete_log(a, b, p, order=None, max_iterations=10000):
        """
        Реализация ρ-метода Полларда для дискретного логарифмирования
        
        Параметры:
            a - основание
            b - значение
            p - модуль (простое число)
            order - порядок элемента a (если известен)
            max_iterations - максимальное число итераций
            
        Возвращает:
            x - решение уравнения или None
        """
        
        # Если порядок не указан, используем p-1
        if order is None:
            order = p - 1
        
        # Ветвящееся отображение
        def branching_function(c, alpha, beta):
            """
            Ветвящееся отображение f
            Возвращает (новый c, новый alpha, новый beta)
            """
            if c < p // 2:
                # f(c) = a*c mod p
                new_c = (a * c) % p
                new_alpha = (alpha + 1) % order
                new_beta = beta
            else:
                # f(c) = b*c mod p
                new_c = (b * c) % p
                new_alpha = alpha
                new_beta = (beta + 1) % order
            return new_c, new_alpha, new_beta
        
        # Шаг 1: Инициализация случайными значениями
        alpha1 = random.randint(0, order - 1)
        beta1 = random.randint(0, order - 1)
        c1 = (pow(a, alpha1, p) * pow(b, beta1, p)) % p
        
        # Начальные значения для "зайца" (такие же)
        alpha2, beta2 = alpha1, beta1
        c2 = c1
        
        print("\n" + "="*60)
        print("НАЧАЛО АЛГОРИТМА ρ-МЕТОДА ПОЛЛАРДА")
        print("="*60)
        print(f"Начальные значения:")
        print(f"  c1 = {c1}, log(c1) = {alpha1} + {beta1} * x")
        print(f"  c2 = {c2}, log(c2) = {alpha2} + {beta2} * x")
        print("-"*60)
        
        # Шаг 2: Поиск коллизии (черепаха и заяц)
        for iteration in range(1, max_iterations + 1):
            # Черепаха: один шаг
            c1, alpha1, beta1 = branching_function(c1, alpha1, beta1)
            
            # Заяц: два шага
            c2, alpha2, beta2 = branching_function(c2, alpha2, beta2)
            c2, alpha2, beta2 = branching_function(c2, alpha2, beta2)
            
            # Вывод первых 5 итераций для отладки
            if iteration <= 5:
                print(f"Итерация {iteration}:")
                print(f"  c1 = {c1:3d}, log(c1) = {alpha1:3d} + {beta1:3d} * x")
                print(f"  c2 = {c2:3d}, log(c2) = {alpha2:3d} + {beta2:3d} * x")
            
            # Проверка коллизии
            if c1 == c2:
                print(f"\n✓ КОЛЛИЗИЯ НАЙДЕНА на итерации {iteration}")
                print(f"  c1 = c2 = {c1}")
                print(f"  log(c1) = {alpha1} + {beta1} * x")
                print(f"  log(c2) = {alpha2} + {beta2} * x")
                print("-"*60)
                
                # Шаг 3: Решение линейного сравнения
                # Уравнение: alpha1 + beta1*x ≡ alpha2 + beta2*x (mod order)
                # => (beta1 - beta2)*x ≡ (alpha2 - alpha1) (mod order)
                
                A = (beta1 - beta2) % order
                B = (alpha2 - alpha1) % order
                
                print(f"Получено уравнение:")
                print(f"  {A} * x ≡ {B} (mod {order})")
                
                # Проверка существования решения
                if A == 0:
                    if B == 0:
                        print("  Уравнение имеет бесконечно много решений")
                        return 0
                    else:
                        print("  Уравнение не имеет решений")
                        return None
                
                # Находим НОД(A, order)
                g, _, _ = DiscreteLogarithmSolver.extended_gcd(A, order)
                
                if B % g != 0:
                    print(f"  Уравнение не имеет решений: {g} не делит {B}")
                    return None
                
                # Приводим уравнение
                A_reduced = A // g
                B_reduced = B // g
                order_reduced = order // g
                
                print(f"  После деления на НОД {g}:")
                print(f"  {A_reduced} * x ≡ {B_reduced} (mod {order_reduced})")
                
                # Находим обратный элемент к A_reduced
                inv = DiscreteLogarithmSolver.mod_inverse(A_reduced, order_reduced)
                if inv is None:
                    print("  Не удалось найти обратный элемент")
                    return None
                
                print(f"  Обратный к {A_reduced} по модулю {order_reduced}: {inv}")
                
                # Частное решение
                x0 = (B_reduced * inv) % order_reduced
                print(f"  Частное решение: x ≡ {x0} (mod {order_reduced})")
                
                # Проверяем все возможные решения
                solutions = []
                for k in range(g):
                    x_candidate = (x0 + k * order_reduced) % order
                    if pow(a, x_candidate, p) == b:
                        solutions.append(x_candidate)
                
                if solutions:
                    print(f"  Найдены решения: {solutions}")
                    # Возвращаем наименьшее положительное решение
                    return min(solutions)
                else:
                    print("  Найденные кандидаты не удовлетворяют уравнению")
                    return None
        
        print(f"\n✗ Коллизия не найдена за {max_iterations} итераций")
        return None
    
    @staticmethod
    def solve_equation(a, b, p, order=None):
        """
        Основная функция для решения уравнения a^x ≡ b (mod p)
        """
        print("\n" + "="*60)
        print(f"РЕШЕНИЕ УРАВНЕНИЯ: {a}^x ≡ {b} (mod {p})")
        print("="*60)
        
        x = DiscreteLogarithmSolver.pollard_rho_discrete_log(a, b, p, order)
        
        print("\n" + "="*60)
        if x is not None:
            print(f"РЕЗУЛЬТАТ: x = {x}")
            print(f"Проверка: {a}^{x} mod {p} = {pow(a, x, p)}")
            print(f"Ожидаемое значение: {b}")
            
            if pow(a, x, p) == b:
                print("✓ РЕШЕНИЕ ВЕРНОЕ!")
            else:
                print("✗ Решение не удовлетворяет уравнению")
        else:
            print("РЕШЕНИЕ НЕ НАЙДЕНО")
        print("="*60)
        
        return x


def main_menu():
    """Главное меню программы"""
    print("="*60)
    print("ЛАБОРАТОРНАЯ РАБОТА №7")
    print("Дискретное логарифмирование в конечном поле")
    print("ρ-метод Полларда")
    print("="*60)
    
    solver = DiscreteLogarithmSolver()
    
    while True:
        print("\n" + "="*60)
        print("ГЛАВНОЕ МЕНЮ")
        print("="*60)
        print("1. Решить пример из методички")
        print("2. Решить индивидуальное задание")
        print("3. Решить произвольное уравнение")
        print("4. Выйти из программы")
        
        try:
            choice = int(input("\nВыберите действие (1-4): "))
            
            if choice == 1:
                # Пример из методички
                solve_example_from_manual(solver)
                
            elif choice == 2:
                # Индивидуальное задание
                solve_individual_task(solver)
                
            elif choice == 3:
                # Произвольное уравнение
                solve_custom_equation(solver)
                
            elif choice == 4:
                print("\nВыход из программы. До свидания!")
                break
                
            else:
                print("Неверный выбор. Попробуйте снова.")
                
        except ValueError:
            print("Пожалуйста, введите число от 1 до 4")
        except KeyboardInterrupt:
            print("\n\nПрограмма прервана пользователем.")
            break


def solve_example_from_manual(solver):
    """Решение примера из методички"""
    print("\n" + "="*60)
    print("ПРИМЕР ИЗ МЕТОДИЧКИ")
    print("="*60)
    print("Уравнение: 10^x ≡ 64 (mod 107)")
    print("Порядок элемента 10 по модулю 107: 53")
    print("Ожидаемое решение: x = 20")
    print("="*60)
    
    p = 107
    a = 10
    b = 64
    order = 53
    
    x = solver.solve_equation(a, b, p, order)
    
    if x is not None and x == 20:
        print("\n✓ Пример успешно решен!")
    elif x is not None:
        print(f"\n! Найдено решение x = {x}, но ожидалось x = 20")
    else:
        print("\n✗ Не удалось решить пример")


def solve_individual_task(solver):
    """Решение индивидуального задания"""
    print("\n" + "="*60)
    print("ИНДИВИДУАЛЬНОЕ ЗАДАНИЕ")
    print("="*60)
    print("Получите параметры у преподавателя и введите их ниже:")
    
    try:
        p = int(input("Введите простое число p: "))
        a = int(input("Введите основание a: "))
        b = int(input("Введите значение b: "))
        
        # Порядок элемента (если известен)
        order_input = input("Введите порядок элемента a (если неизвестен, нажмите Enter): ")
        if order_input.strip() == "":
            order = None
            print("Порядок не указан, используется p-1")
        else:
            order = int(order_input)
        
        solver.solve_equation(a, b, p, order)
        
    except ValueError:
        print("Ошибка ввода! Пожалуйста, вводите целые числа.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def solve_custom_equation(solver):
    """Решение произвольного уравнения"""
    print("\n" + "="*60)
    print("РЕШЕНИЕ ПРОИЗВОЛЬНОГО УРАВНЕНИЯ")
    print("="*60)
    
    try:
        p = int(input("Введите простое число p: "))
        a = int(input("Введите основание a: "))
        b = int(input("Введите значение b: "))
        
        order_input = input("Введите порядок элемента a (опционально): ")
        order = int(order_input) if order_input.strip() else None
        
        solver.solve_equation(a, b, p, order)
        
    except ValueError:
        print("Ошибка ввода! Пожалуйста, вводите целые числа.")


if __name__ == "__main__":
    main_menu()