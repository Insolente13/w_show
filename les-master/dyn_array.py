import ctypes


class DynArray:

    def __init__(self):
        self.count = 0
        self.capacity = 16
        self.array = self.make_array(self.capacity)

    def __len__(self):
        return self.count

    def make_array(self, new_capacity):
        return (new_capacity * ctypes.py_object)()

    def __getitem__(self, i):
        if i < 0 or i >= self.count:
            raise IndexError('Index is out of bounds')
        return self.array[i]

    def resize(self, new_capacity):
        new_array = self.make_array(new_capacity)
        for i in range(self.count):
            new_array[i] = self.array[i]
        self.array = new_array
        self.capacity = new_capacity

    def append(self, itm):
        if self.count == self.capacity:
            self.resize(2 * self.capacity)
        self.array[self.count] = itm
        self.count += 1
    '''4.1. Добавьте метод insert(i, itm), который вставляет в i-ю 
    позицию объект itm, сдвигая вперёд все последующие элементы. 
    Учтите, что новая длина массива может превысить размер буфера.'''
    def insert(self, i, itm):
        if self.count >= i >= 0:
            if self.count == self.capacity:
                self.resize(2 * self.capacity)
            new_array = self.array[:i] + [itm] + self.array[i:self.count]
            for elements in range(self.count+1):
                self.array[elements] = new_array[elements]
            self.count += 1
        else:
            raise IndexError('Index is out of bounds')

    '''4.2. Добавьте метод delete(i), который удаляет 
    объект из i-й позиции, при необходимости сжимая буфер.
    В обоих случаях, если индекс i лежит вне допустимых границ, генерируйте исключение.
    Важно, единственное исключение: для метода insert() параметр i может принимать значение, 
    равное длине рабочего массива count, в таком случае добавление происходит в его хвост.'''
    def delete(self, i):
        if i == 0 and self.count > 0:
            new_array = self.array[1:self.count]
        elif self.count > i and self.count > 0:
            new_array = self.array[:i] + self.array[i + 1:self.count]
        elif self.count == i and self.count > 0:
            new_array = self.array[:i]
        else:
            raise IndexError('Index is out of bounds')

        self.array = self.make_array(self.capacity)
        for elements in range(self.count - 1):
            self.array[elements] = new_array[elements]

        self.count -= 1

        if self.count != 0 and self.count == int((self.capacity / 2) - 1) and int((self.capacity * 2) / 3) > 16:
            self.capacity = int((self.capacity * 2) / 3)
            self.resize(self.capacity)
        elif int((self.capacity * 2) / 3) <= 16:
            self.capacity = 16
            self.resize(self.capacity)


'''4.4. Напишите тесты, проверяющие работу методов insert() и delete():'''
from random import randint
'''-- вставка элемента, когда в итоге размер
буфера не превышен (проверьте также размер буфера);'''


def test_insert_1():
    count_try = 1000
    count = 0
    for c_try in range(count_try):
        test_da = DynArray()
        random_range = randint(0, 15)

        for x in range(random_range):
            test_da.append(x)
        test_da.insert(randint(0, random_range), randint(0, 100))
        if test_da.capacity >= test_da.count:
            count += 1
    if count != count_try:
        print('FAIL')
    else:
        print('PASSED')


'''-- вставка элемента, когда в результате превышен размер
буфера (проверьте также корректное изменение размера буфера);'''


def test_insert_2():
    count_try = 100
    count = 0
    for c_try in range(count_try):
        test_da = DynArray()
        random_range = 16 * (2 ** randint(1, 5))
        for x in range(random_range):
            test_da.append(x)
        first_capacity = test_da.capacity
        test_da.insert(random_range, randint(1, 5))

        if test_da.capacity / first_capacity == 2:
            count += 1
    if count != count_try:
        print('FAIL')
    else:
        print('PASSED')


'''-- попытка вставки элемента в недопустимую позицию;'''


def test_insert_3():
    test_da = DynArray()
    random_range = randint(0, 50)
    for x in range(random_range):
        test_da.append(x)
    try:
        test_da.insert(random_range + 1, randint(0, 50))
        print('FAIL')
    except IndexError:
        print('PASSED')


'''-- удаление элемента, когда в результате размер
буфера остаётся прежним (проверьте также размер буфера);'''


def test_delete_1():
    pass


'''-- удаление элемента, когда в результате понижается размер
буфера (проверьте также корректное изменение размера буфера);'''


def test_delete_2():
    test_da = DynArray()
    for x in range(1047):
        test_da.append(x)

    count_array = test_da.count
    len_array = test_da.capacity

    if len_array == 2048 and count_array == 1047:
        for y in range(1001):
            test_da.delete(0)

    len_new_array = test_da.capacity
    count_new_array = test_da.count

    if len_new_array == 79 and count_new_array == 46:
        print('PASSED')
    else:
        print('FAIL')


'''-- попытка удаления элемента в недопустимой позиции.'''


def test_delete_3():
    test_da = DynArray()
    random_range = randint(0, 1000)
    for x in range(random_range):
        test_da.append(x)
    try:
        test_da.delete(random_range + 1)
        print('FAIL')
    except IndexError:
        print('PASSED')
