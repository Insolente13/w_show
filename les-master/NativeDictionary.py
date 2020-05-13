class NativeDictionary:
    def __init__(self, sz):
        self.size = sz
        self.slots = [None] * self.size
        self.values = [None] * self.size

    def hash_fun(self, key):
        index = 0
        for x in range(len(key)):
            index += ord(key[x]) * (x + 1)
        # в качестве key поступают строки!
        # всегда возвращает корректный индекс слота
        return index % self.size

    def is_key(self, key):
        hf = self.hash_fun(key)
        if self.slots[hf] == key:
            return True
        else:
            for x in range(self.size):
                if self.slots[x] == key:
                    return True
        # возвращает True если ключ имеется,
        # иначе False
        return False

    def put(self, key, value):
        key_hash = self.hash_fun(key)
        if self.slots[key_hash] == key:
            self.values[key_hash] = value
        elif self.slots[key_hash] is None:
            self.values[key_hash] = value
            self.slots[key_hash] = key
        else:
            for x in range(self.size):
                if self.slots[x] is None:
                    self.slots[x] = key
                    self.values[x] = value
                    break
        # гарантированно записываем
        # значение value по ключу key

    def get(self, key):
        key_hash = self.hash_fun(key)

        if self.slots[key_hash] == key:
            return self.values[key_hash]
        else:
            for x in range(self.size):
                if self.slots[x] == key:
                    return self.values[x]
        # возвращает value для key,
        # или None если ключ не найден
        return None
