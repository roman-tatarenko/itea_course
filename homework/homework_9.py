"""
Давайте поэкспериментируем с параллельным выполнением задач.
Напишите функцию,которая внутри себя будет собирать список с числами от 0 до 100_000_000.

Далее напишите код, который будет последовательно 3 раза вызывать эту функцию и измерьте
получившееся время выполнения с помощью модуля time или datetime.

Далее перепишите код таким образом,чтобы распараллелить трёхкратное выполнение с использованием потоков
или процессов на свой вкус и добейтесь ускорения работы программы. Измерьте время выполнения и
прикрепите результаты измерений к получившемуся коду в виде комментария. Желаю удачи!)
"""

import datetime
import os
import time
from threading import Thread


def list_of_numbers_function():
    list_of_numbers = list()
    number = 0
    while number <= 100000000:
        list_of_numbers.append(number)
        number += 1
    time.sleep(2)
    return list_of_numbers


print(f"{os.getpid()}")
start = datetime.datetime.now()
first = list_of_numbers_function()
second = list_of_numbers_function()
third = list_of_numbers_function()
end = datetime.datetime.now()
timer = (end - start).microseconds
print(f"Время выполнения последовательно =  {timer} микросекунд")

start = datetime.datetime.now()
for thread in range(3):
    print(f"{os.getpid()}")
    t = Thread(target=list_of_numbers_function)
    t.start()
    t.join()
end = datetime.datetime.now()
timer = (end - start).microseconds
print(f"Время выполнения параллельно =  {timer} микросекунд")
