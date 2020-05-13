class Queue:
    def __init__(self):
        self.stack = []
        # инициализация хранилища данных

    def enqueue(self, item):
        self.stack.append(item)
        # вставка в хвост

    def dequeue(self):
        if self.size() > 0:
            return self.stack.pop(0)
        return None # если очередь пустая

    def size(self):
        return len(self.stack) # размер очереди

    '''6.3. Напишите функцию, которая "вращает" очередь по кругу на N элементов.'''
    def circle(self, count):
        for x in range(count):
            self.enqueue(self.dequeue())
