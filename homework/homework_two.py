"""
1. Написать декоратор, который будет печатать на экран время работы функции (пользуемся datetime).
"""

# Декоратор - паттерн проектирования, который позволяет изменить поведение функции без переписывания ее структуры.
import datetime


def time_execution(function):
    def inner(*args, **kwargs):
        start = datetime.datetime.now()
        result = function(*args, **kwargs)
        end = datetime.datetime.now()
        timer = (end - start).microseconds
        print(f"Время выполнения функции =  {timer} микросекунд")
        return result
    return inner


@time_execution
def summarizer(a, b):
    return a + b


res = summarizer(5, 5)

"""
2. Написать функцию для вычислений ряда чисел Фибоначчи (можно через цикл, можно через рекурсию).
"""


# Fn = Fn-1 + Fn-2
@time_execution
def fibonachi_list(n) -> int:
    try:

        x = 0
        y = 1
        for i in range(n):
            yield x
            y = x + y
            x = y - x
    except TypeError:
        raise TypeError("ERROR! Iterator must be integer!")


# print(list(fibonachi_list(8)))

"""
3. Реализовать функцию, которая принимает три позиционных аргумента и возвращает сумму наибольших двух из них
(если вы решили сравнивать все 3 числа между собой вручную - это очень плохая идея :) ).
"""


def two_of_three(x, y, z):
    array = [x, y, z]
    new = list()
    a = max(array)
    new.append(a)
    array.remove(a)
    b = max(array)
    return a + b


# sum = two_of_three(35, 4, 66)
# print(sum)
