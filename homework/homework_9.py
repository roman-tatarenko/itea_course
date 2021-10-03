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


# Comment for Nikolas Luchanos:
# Я так и не смог добиться ускорения работы программы -> мне кажется что этому мешает GIL, так как фрозит
# некоторые параметры. Может я неправ. Потратил на это очень много времени, но скорость не была увеличена.
# Когда у себя запускал твой код из классной работы -> возникала ошибка:
# RuntimeError:
#         An attempt has been made to start a new process before the
#         current process has finished its bootstrapping phase.
#
#         This probably means that you are not using fork to start your
#         child processes and you have forgotten to use the proper idiom
#         in the main module:
#
#             if __name__ == '__main__':
#                 freeze_support()

# Решается конструкцией:
# if __name = '__main__':
# С чем это связано? И как, все-таки, увеличить скорость выполнения программы?

def time_execution(function):
    def inner(*args, **kwargs):
        start_time = datetime.datetime.now()
        result = function(*args, **kwargs)
        end_time = datetime.datetime.now()
        stopwatch = (end_time - start_time).microseconds
        print(f"Время выполнения функции =  {stopwatch} микросекунд")
        return result

    return inner


@time_execution
def list_of_numbers_function():
    print(f"This function executing into process {os.getpid()}")
    list_of_numbers = list()
    number = 0
    while number <= 100000000:
        list_of_numbers.append(number)
        number += 1
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

start = datetime.datetime.now()
# if __name__ == '__main__':
p_0 = multiprocessing.Process(target=list_of_numbers_function)
p_1 = multiprocessing.Process(target=list_of_numbers_function)
p_2 = multiprocessing.Process(target=list_of_numbers_function)
p_0.start()
p_1.start()
p_2.start()

p_0.join()
p_1.join()
p_2.join()

end = datetime.datetime.now()
timer = (end - start).microseconds
print(f"Время выполнения функции =  {timer} микросекунд")
