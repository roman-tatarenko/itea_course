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
import multiprocessing
import os
import threading
from multiprocessing import Process
from threading import Thread


def time_execution(function):
    def inner(*args, **kwargs):
        start = datetime.datetime.now()
        result = function(*args, **kwargs)
        end = datetime.datetime.now()
        timer = (end - start).microseconds
        print(f"Время выполнения функции =  {timer} микросекунд")
        return result

    return inner


def list_of_numbers_function():
    list_of_numbers = list()
    for x in range(5):
        list_of_numbers.append(x)
    return list_of_numbers


print("---------------")
start = datetime.datetime.now()
for x in range(3):
    print(f"Process id is {os.getpid()}")
    call_of_func = list_of_numbers_function()
    print(call_of_func)
end = datetime.datetime.now()
timer = (end - start).microseconds
print(f"Время выполнения функции =  {timer} микросекунд")
print("===============")



print()
print("***************")

print(f"Process id is {os.getpid()}")
start = datetime.datetime.now()
p_0 = multiprocessing.Process(target=list_of_numbers_function, args=())

p_0.start()

p_0.join()

end = datetime.datetime.now()
timer = (end - start).microseconds
print(f"Время выполнения функции =  {timer} микросекунд")
print("ˆˆˆˆˆˆˆˆˆˆˆˆ")
