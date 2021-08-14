""""
Homework:
Написать программу, которая запрашивает у пользователя строку чисел, разделённых пробелом.
При нажатии Enter должна выводиться сумма чисел. Пользователь может продолжить ввод чисел, разделённых пробелом
и снова нажать Enter. Сумма вновь введённых чисел будет добавляться к уже подсчитанной сумме.
Но если вместо числа вводится специальный символ, выполнение программы завершается.
Если специальный символ введён после нескольких чисел, то вначале нужно добавить сумму этих чисел к полученной
ранее сумме и после этого завершить программу.
"""


def sum_numbers():
    try:
        numbers = input('Введите строку чисел, разделённых пробелом и нажмите Enter для продолжения: ').strip()
        total_sum = sum([int(i) for i in numbers.split(' ')])
        print(f'Сумма чисел = {total_sum}')
        end_program = False
        while end_program is False:
            new_numbers = input('Для завершения программы введите символ q или введите строку чисел, разделённых '
                                'пробелом и нажмите Enter для продолжения: ').split(' ')

            if 'q' in new_numbers:
                temporary_sum = 0
                for i in range(len(new_numbers)):
                    if new_numbers[i] == 'q':
                        break
                    else:
                        temporary_sum = temporary_sum + sum([int(i) for i in new_numbers[i]])
                total_sum = total_sum + temporary_sum
                print(f'Сумма чисел = {total_sum}')
                end_program = True
                print('Выполнение программы остановлено')
            else:
                temporary_sum = sum([int(i) for i in new_numbers])
                total_sum = total_sum + temporary_sum
                print(f'Сумма чисел = {total_sum}')
        return total_sum
    except ValueError:
        print('Инцидент! Программа завершена аварийно, ошибка ожидаемых данных')


sum_numbers()
