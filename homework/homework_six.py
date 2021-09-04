"""
Реализуйте базовый класс Car.
У класса должны быть следующие атрибуты: speed, color, name, is_police (булево).
А также методы: go, stop, turn(direction), которые должны сообщать, что машина поехала, остановилась, повернула (куда);
опишите несколько дочерних классов: TownCar, SportCar, WorkCar, PoliceCar;
добавьте в базовый класс метод show_speed, который должен показывать текущую скорость автомобиля;
для классов TownCar и WorkCar переопределите метод show_speed. При значении скорости свыше 60 (TownCar) и
40 (WorkCar) должно выводиться сообщение о превышении скорости.
Реализовать метод для user-friendly вывода информации об автомобиле.
"""


class Car:
    def __init__(self, speed, color, name, is_police):
        self.speed = speed
        self.color = color
        self.name = name
        self.is_police = is_police

    @staticmethod
    def go():
        print("Машина поехала.")

    @staticmethod
    def stop():
        print("Машина остановилась.")

    @staticmethod
    def turn(direction):
        if direction == "right":
            print("Машина повернула напрво.")
        elif direction == "left":
            print("Машина повернула налево.")

    def show_speed(self):
        print(f"Текущая скорость атомобиля = {self.speed}")

    def show_info(self):
        print(f"Модель машины: {self.name}\n"
              f"Цвет машины: {self.color}\n"
              f"Текущая скорость машины: {self.speed}\n"
              f"Машина полиции: {self.is_police}")


class TownCar(Car):
    def show_speed(self):
        if self.speed > 60:
            print(f"Превышена разрешенная скорость на {self.speed - 60} км/ч")


class SportCar(Car):
    pass


class WorkCar(Car):
    def show_speed(self):
        if self.speed > 40:
            print(f"Превышена разрешенная скорость на {self.speed - 40} км/ч")


class PoliceCar(Car):
    pass


car = TownCar(
    speed=61,
    color="green",
    name="Toyota",
    is_police=False)

car.show_info()
car.go()
car.turn("left")
car.turn("right")
car.stop()
car.show_speed()

print()

car = PoliceCar(
    speed=90,
    color="green",
    name="Toyota",
    is_police=True)

car.show_info()
car.go()
car.turn("left")
car.turn("right")
car.stop()
car.show_speed()
