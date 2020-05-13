class HashTable:
    def __init__(self, sz, stp):
        self.size = sz
        self.step = stp
        self.slots = [None] * self.size

    def hash_fun(self, value):
        index = 0
        for x in range(len(value)):
            index += ord(value[x]) * (x + 1)
        # в качестве value поступают строки!
        # всегда возвращает корректный индекс слота
        return index % self.size

    def seek_slot(self, value):
        hf_index = self.hash_fun(value)

        if self.slots[hf_index] is None:
            return hf_index
        else:
            for x in range(self.size):
                if self.slots[x] is None:
                    return x
        # находит индекс пустого слота для значения, или None
        return None

    def put(self, value):
        to_put = self.seek_slot(value)
        if to_put is not None:
            self.slots[to_put] = value
        return to_put
        # записываем значение по хэш-функции
        # возвращается индекс слота или None,
        # если из-за коллизий элемент не удаётся
        # разместить

    def find(self, value):
        f_index = self.hash_fun(value)
        if self.slots[f_index] == value:
            return f_index
        else:
            for x in range(self.size):
                if self.slots[x] == value:
                    return x
        # находит индекс слота со значением, или None
        return None

