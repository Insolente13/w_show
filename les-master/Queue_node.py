class Stack:
    def __init__(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    def push(self, element):
        self.stack.insert(self.size(), element)

    def pop(self):
        if len(self.stack) > 0:
            return self.stack.pop(0)
        else:
            return None

    def peek(self):
        if len(self.stack) > 0:
            return self.stack[-1]
        else:
            return None


class Queue:
    def __init__(self):
        self.stack_1 = Stack()
        self.stack_2 = Stack()
        # инициализация хранилища данных

    def enqueue(self, item):
        self.stack_1.push(item)
        # вставка в хвост

    def dequeue(self):
        if self.stack_2.size() == 0 and self.stack_1.size() != 0:
            while self.stack_1.size() != 0:
                self.stack_2.push(self.stack_1.pop())

        return self.stack_2.pop()
        # выдача из головы

    def size(self):
        return self.stack_1.size() + self.stack_2.size()  # размер очереди

    '''6.3. Напишите функцию, которая "вращает" очередь по кругу на N элементов.'''
    def circle(self, count):
        for x in range(count):
            self.enqueue(self.dequeue())

            
