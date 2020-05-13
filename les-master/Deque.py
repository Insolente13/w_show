class Deque:
    def __init__(self):
        self.stack = []
        # инициализация внутреннего хранилища

    def addFront(self, item):
        self.stack.insert(0, item)
        # добавление в голову

    def addTail(self, item):
        self.stack.append(item)

        # добавление в хвост

    def removeFront(self):
        # удаление из головы
        if len(self.stack) > 0:
            return self.stack.pop(0)
        else:
            return None  # если очередь пуста

    def removeTail(self):
        if len(self.stack) > 0:
            return self.stack.pop()
        else:
            return None  # если очередь пуста

    def size(self):
        return len(self.stack)  # размер очереди


'''7.2. Напишите функцию, которая с помощью deque проверяет, 
является ли некоторая строка палиндромом 
(читается одинаково слева направо и справа налево).'''
def palindrome(word):
    pal_dq = Deque()
    for w in word:
        pal_dq.addFront(w)
    for char in range(pal_dq.size()):
        if pal_dq.removeFront() != pal_dq.removeTail():
            print('Not palindrome!')
            return
    print('Palindrome')


# Тесты

def test_addFront():
    dq = Deque()
    for x in 'anywords':
        dq.addFront(x)

    dq_fs = dq.size()
    random_symbol = 1000

    dq.addFront(random_symbol)

    if (dq.size() != (dq_fs + 1)) or dq.stack[0] != random_symbol:
        print('FAIL')
    else:
        print('PASSED')


def test_addTail():
    dq = Deque()
    for x in 'anywords':
        dq.addTail(x)

    dq_fs = dq.size()
    random_symbol = 1000

    dq.addTail(random_symbol)

    if (dq.size() != (dq_fs + 1)) or dq.stack[-1] != random_symbol:
        print('FAIL')
    else:
        print('PASSED')


def test_removeFront():
    dq = Deque()
    word_to_check = 'anywords'
    for x in word_to_check:
        dq.addFront(x)

    dq_fs = dq.size()
    del_symbol = dq.removeFront()

    if (dq.size() != (dq_fs - 1)) \
            or (del_symbol in dq.stack)\
            or (del_symbol == dq.stack[0]):
        print(dq.stack, word_to_check)
        print('FAIL')
    else:
        print('PASSED')


def test_removeTail():
    dq = Deque()
    word_to_check = 'anywords'
    for x in word_to_check:
        dq.addTail(x)

    dq_fs = dq.size()
    del_symbol = dq.removeTail()

    if (dq.size() != (dq_fs - 1)) \
            or (del_symbol in dq.stack) \
            or (del_symbol == dq.stack[-1]):
        print('FAIL')
    else:
        print('PASSED')

