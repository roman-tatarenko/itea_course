""""
Покрыть тестами функции из прошлого ДЗ:
- Вычислятель чисел Фибоначчи.
- Функция, которая возвращает сумму наибольших двух из трех переданных чисел.


Примечания:
- функции должны тестироваться в разных тестовых кейсах;
- обязательно нужно покрыть тестами, как позитивные, так и негативные кейсы.
- обязательно нужно покрыть тестами особые случаи.
- обязательно используйте parametrize для задания сразу нескольких тестовых кейсов в рамках одной тестовой функции.


Дополнительное задание со звездочкой: в своём репозитории ограничить возможность делать merge
в main ветку до тех пор, пока кто-то из collaborators не поставить approve к пул-риквесту.
"""

import pytest

from homework.homework_two import fibonachi_list, two_of_three


class TestFibonachiFunction:
    @pytest.mark.parametrize('value, result',
                             [
                                 pytest.param(0, [],
                                              id="if n is 0"),
                                 pytest.param(False, [],
                                              id="if n is False"),
                                 pytest.param(1, [0],
                                              id="if n is 1"),
                                 pytest.param(True, [0],
                                              id="if n is True"),
                                 pytest.param(11, [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55],
                                              id="if n is 1")
                             ])
    def test_check_on_possibility_make_fibonachi_list(self, value, result):
        fibo_list = list(fibonachi_list(n=value))
        assert fibo_list == result

    @pytest.mark.parametrize('value',
                             [
                                 pytest.param(36.6,
                                              id="if n is float"),

                                 pytest.param("5",
                                              id="if n is string")
                             ])
    def test_check_on_impossibility_make_fibonachi_list_with_invalid_datatype(self, value):
        with pytest.raises(TypeError):
            list(fibonachi_list(n=value))

    def test_check_on_impossibility_make_fibonachi_list_with_negative_numeric(self):
        fibo_list = list(fibonachi_list(n=-7))
        assert fibo_list == []


class TestTwoOfThreeFunction:
    @pytest.mark.parametrize('x, y, z, result',
                             [
                                 pytest.param(3, 4, 5, 9,
                                              id="if value is integer"),

                                 pytest.param(3.3, 4.4, 5.5, 9.9,
                                              id="if value is float")
                             ])
    def test_check_on_possibility_sum_biggest_numbers(self, x, y, z, result):
        test_sum = two_of_three(x, y, z)
        assert test_sum == result

    @pytest.mark.parametrize('x,y,z',
                             [
                                 pytest.param("3", 4, 5,
                                              id="if one of number is string"),
                                 pytest.param(3, None, 5,
                                              id="if one of number is None")
                             ])
    def test_check_on_impossibility_sum_biggest_numbers_with_invalid_dtatype(self, x, y, z):
        with pytest.raises(TypeError):
            two_of_three(x, y, z)

    def test_check_on_impossibility_sum_biggest_numbers(self):
        test_sum = two_of_three(3, -4, -5)
        assert test_sum == -1
