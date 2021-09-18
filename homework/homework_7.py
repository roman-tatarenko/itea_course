"""
Реализовать класс матрицы произвольного типа. При создании экземпляра передаётся вложенный список. Для объектов
класса реализовать метод сложения и вычитания матриц, их сравнения друг с другом, а также умножения, деления матрицы
на число и user-friendly вывода матрицы на экран.
"""


class Matrix:
    def __init__(self, some_matrix):
        self.some_matrix = some_matrix

    def __str__(self):
        return f"Ваша матрица \n" + '\n'.join('\t'.join(map(str, row)) for row in self.some_matrix)

    def __add__(self, other):
        if isinstance(other, Matrix):
            new_matrix = []
            for i in range(len(self.some_matrix)):
                new_matrix.append([])
                for i_1 in range(len(self.some_matrix[i])):
                    new_matrix[i].append(self.some_matrix[i][i_1] + other.some_matrix[i][i_1])
            return Matrix(new_matrix)

    def __sub__(self, other):
        if isinstance(other, Matrix):
            new_matrix = []
            for i in range(len(self.some_matrix)):
                new_matrix.append([])
                for i_1 in range(len(self.some_matrix[i])):
                    new_matrix[i].append(self.some_matrix[i][i_1] - other.some_matrix[i][i_1])
            return Matrix(new_matrix)

    def __mul__(self, other):
        if isinstance(other, Matrix):
            new_matrix = []
            for i in range(len(self.some_matrix)):
                new_matrix.append([])
                for i_1 in range(len(self.some_matrix[i])):
                    new_matrix[i].append(self.some_matrix[i][i_1] * other.some_matrix[i][i_1])
            return Matrix(new_matrix)

    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            new_matrix = []
            for i in range(len(self.some_matrix)):
                new_matrix.append([])
                for i_1 in range(len(self.some_matrix[i])):
                    new_matrix[i].append(self.some_matrix[i][i_1] / other)
            return Matrix(new_matrix)

    def __eq__(self, other):
        if isinstance(other, Matrix):
            new_matrix = []
            for i in range(len(self.some_matrix)):
                new_matrix.append([])
                for i_1 in range(len(self.some_matrix[i])):
                    new_matrix[i].append(self.some_matrix[i][i_1] == other.some_matrix[i][i_1])
            return Matrix(new_matrix)


a = Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
b = Matrix([[11, 22, 33], [44, 55, 66], [77, 88, 99]])
c = a == b
print(c)
