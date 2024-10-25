"""
Задача "Потоки гостей в кафе":
Необходимо имитировать ситуацию с посещением гостями кафе.
Создайте 3 класса: Table, Guest и Cafe.
Класс Table:
Объекты этого класса должны создаваться следующим способом - Table(1)
Обладать атрибутами number - номер стола и guest - гость, который сидит за этим столом (по умолчанию None)
Класс Guest:
Должен наследоваться от класса Thread (быть потоком).
Объекты этого класса должны создаваться следующим способом - Guest('Vasya').
Обладать атрибутом name - имя гостя.
Обладать методом run, где происходит ожидание случайным образом от 3 до 10 секунд.
Класс Cafe:
Объекты этого класса должны создаваться следующим способом - Cafe(Table(1), Table(2),....)
Обладать атрибутами queue - очередь (объект класса Queue) и tables - столы в этом кафе (любая коллекция).
Обладать методами guest_arrival (прибытие гостей) и discuss_guests (обслужить гостей).
Метод guest_arrival(self, *guests):
Должен принимать неограниченное кол-во гостей (объектов класса Guest).
Далее, если есть свободный стол, то садить гостя за стол (назначать столу guest), запускать поток гостя и выводить на экран строку "<имя гостя> сел(-а) за стол номер <номер стола>".
Если же свободных столов для посадки не осталось, то помещать гостя в очередь queue и выводить сообщение "<имя гостя> в очереди".
Метод discuss_guests(self):
Этот метод имитирует процесс обслуживания гостей.
Обслуживание должно происходить пока очередь не пустая (метод empty) или хотя бы один стол занят.
Если за столом есть гость(поток) и гость(поток) закончил приём пищи(поток завершил работу - метод is_alive), то вывести строки "<имя гостя за текущим столом> покушал(-а) и ушёл(ушла)" и "Стол номер <номер стола> свободен". Так же текущий стол освобождается (table.guest = None).
Если очередь ещё не пуста (метод empty) и стол один из столов освободился (None), то текущему столу присваивается гость взятый из очереди (queue.get()). Далее выводится строка "<имя гостя из очереди> вышел(-ла) из очереди и сел(-а) за стол номер <номер стола>"
Далее запустить поток этого гостя (start)
Таким образом мы получаем 3 класса на основе которых имитируется работа кафе:
Table - стол, хранит информацию о находящемся за ним гостем (Guest).
Guest - гость, поток, при запуске которого происходит задержка от 3 до 10 секунд.
Cafe - кафе, в котором есть определённое кол-во столов и происходит имитация прибытия гостей (guest_arrival) и их обслуживания (discuss_guests).

Пример результата выполнения программы:
Выполняемый код:
class Table:
...
class Guest:
...
class Cafe:
...
# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()

Вывод на консоль (последовательность может меняться из-за случайного время пребывания гостя):
Maria сел(-а) за стол номер 1
Oleg сел(-а) за стол номер 2
Vakhtang сел(-а) за стол номер 3
Sergey сел(-а) за стол номер 4
Darya сел(-а) за стол номер 5
Arman в очереди
Vitoria в очереди
Nikita в очереди
Galina в очереди
Pavel в очереди
Ilya в очереди
Alexandra в очереди
Oleg покушал(-а) и ушёл(ушла)
Стол номер 2 свободен
Arman вышел(-ла) из очереди и сел(-а) за стол номер 2
.....
Alexandra покушал(-а) и ушёл(ушла)
Стол номер 4 свободен
Pavel покушал(-а) и ушёл(ушла)
Стол номер 3 свободен
Примечания:
Для проверки значения на None используйте оператор is (table.guest is None).
Для добавления в очередь используйте метод put, для взятия - get.
Для проверки пустоты очереди используйте метод empty.
Для проверки выполнения потока в текущий момент используйте метод is_alive.
"""
import random  # Импортируем модуль для генерации случайных чисел
import time  # Импортируем модуль для работы со временем
from threading import Thread  # Импортируем класс Thread для работы с потоками
from queue import Queue  # Импортируем класс Queue для работы с очередями

class Table:
    def __init__(self, number):
        self.number = number  # Номер стола
        self.guest = None  # Гость за столом (по умолчанию None)

class Guest(Thread):
    def __init__(self, name):
        super().__init__()  # Инициализируем родительский класс Thread
        self.name = name  # Имя гостя

    def run(self):
        # Ожидание случайное время от 3 до 10 секунд
        time.sleep(random.randint(3, 10))

class Cafe:
    def __init__(self, *tables):
        self.queue = Queue()  # Инициализируем очередь для гостей
        self.tables = tables  # Список столов в кафе

    def guest_arrival(self, *guests):
        # Метод для обработки прибытия гостей
        for guest in guests:
            # Ищем свободный стол
            free_table = next((table for table in self.tables if table.guest is None), None)
            if free_table:
                # Если есть свободный стол, размещаем гостя
                free_table.guest = guest  # Назначаем гостя столу
                guest.start()  # Запускаем поток гостя
                print(f"{guest.name} сел(-а) за стол номер {free_table.number}")  # Сообщение о посадке
            else:
                # Если свободных столов нет, помещаем гостя в очередь
                self.queue.put(guest)  # Добавляем гостя в очередь
                print(f"{guest.name} в очереди")  # Сообщение о том, что гость в очереди

    def discuss_guests(self):
        # Метод для обслуживания гостей
        while not self.queue.empty() or any(table.guest is not None for table in self.tables):
            # Цикл продолжается, пока очередь не пуста или хотя бы один стол занят
            for table in self.tables:
                if table.guest is not None and not table.guest.is_alive():
                    # Если за столом есть гость и он закончил приём пищи
                    print(f"{table.guest.name} покушал(-а) и ушёл(ушла)")  # Сообщение о том, что гость ушёл
                    print(f"Стол номер {table.number} свободен")  # Сообщение о свободном столе
                    table.guest = None  # Освобождаем стол

                if table.guest is None and not self.queue.empty():
                    # Если стол свободен и очередь не пуста
                    guest_from_queue = self.queue.get()  # Берём гостя из очереди
                    table.guest = guest_from_queue  # Назначаем гостя столу
                    guest_from_queue.start()  # Запускаем поток этого гостя
                    print(f"{guest_from_queue.name} вышел(-ла) из очереди и сел(-а) за стол номер {table.number}")  # Сообщение о посадке

# Создание столов
tables = [Table(number) for number in range(1, 6)]  # Создаём 5 столов

# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]

# Создание гостей
guests = [Guest(name) for name in guests_names]  # Создаём гостей на основе имен

# Заполнение кафе столами
cafe = Cafe(*tables)  # Создаём кафе с заданными столами

# Приём гостей
cafe.guest_arrival(*guests)  # Принимаем гостей в кафе

# Обслуживание гостей
cafe.discuss_guests()  # Начинаем обслуживание гостей