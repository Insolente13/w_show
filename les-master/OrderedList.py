class Node:
    def __init__(self, v):
        self.value = v
        self.prev = None
        self.next = None


class OrderedList:
    def __init__(self, asc):
        self.head = None
        self.tail = None
        self.__ascending = asc

    '''1. Дополнительную опцию asc в конструкторе OrderedList, 
которая указывает, по возрастанию (True) или по убыванию (False) должны храниться элементы в массиве.
Эту опцию сделайте приватной -- изменять её можно только в конструкторе и методе очистки clean().'''

    '''2. Метод сравнения двух значений compare(). 
    В общем случае, мы можем хранить в нашем списке произвольные объекты (например, экземпляры класса Cat), 
    и способ, которым мы желаем их сравнивать, потенциально может быть самым произвольным. 
    Пока сделайте базовый вариант этого метода, который сравнивает числовые значения.'''
    def compare(self, v1, v2):
        if v1 < v2:
            return -1  # -1 если v1 < v2
        elif v1 > v2:
            return 1  # +1 если v1 > v2
        else:
            return 0  # 0 если v1 == v2

    '''3. Добавление нового элемента по значению add() с единственным параметром -- новым добавляемым значением 
    (новый узел для него создавайте внутри метода add). 
    Элемент должен вставиться автоматически между элементами 
    с двумя подходящими значениями (либо в начало или конец списка) 
    с учётом его значения и признака упорядоченности. 
    Используйте для этого метод сравнения значений из предыдущего пункта.'''
    def add(self, value):
        add_node = Node(value)
        # Первое и последнее
        if self.head is None:
            self.head = add_node
            self.tail = add_node
        # Первое или последнее
        elif self.head is not None:
            if self.__ascending is True:
                asc_type = 1
            else:
                asc_type = -1
            if self.compare(add_node.value, self.head.value) * asc_type <= 0:
                head_before = self.head
                add_node.next = head_before
                head_before.prev = add_node
                self.head = add_node
            elif self.compare(add_node.value, self.tail.value) * asc_type >= 0:
                self.tail.next = add_node
                add_node.prev = self.tail
                self.tail = add_node
            # Середина
            else:
                node = self.head
                while node is not None:
                    first_compare = self.compare(add_node.value, node.value) * asc_type
                    second_compare = self.compare(add_node.value, node.next.value) * asc_type

                    if first_compare > 0 and second_compare <= 0:
                        node_next = node.next
                        node_prev = node
                        add_node.prev = node_prev
                        node.next = add_node
                        add_node.next = node_next
                        node_next.prev = add_node

                        break
                    node = node.next
        # автоматическая вставка value
        # в нужную позицию

    def find(self, val):
        node = self.head
        f_node = None
        while node is not None:
            if node.value == val:
                f_node = node
                break
            node = node.next
        return f_node

    def delete(self, val, all=False):
        break_point = 0
        node = self.head

        while node is not None:
            #  удаляем первое и единственное
            if node.value == val and node.next is None and node.prev is None:
                self.head = None
                self.tail = None
                break_point += 1
            #  удаляем первое и НЕ единственное
            elif node.value == val and node.next is not None and node.prev is None:
                self.head = node.next
                self.head.prev = None
                break_point += 1
            #  удаляем последнее и НЕ единственное
            elif node.value != val and node.next is not None:
                if node.next.value == val and node.next.next is None:
                    node.next = None
                    self.tail = node
                    break_point += 1
                elif node.next.value == val and node.next.next is not None:
                    while node.next.value == val and node.next.next is not None:
                        if all is False and break_point != 0:
                            break
                        node.next.next.prev = node
                        node.next = node.next.next
                        break_point += 1

            if all == False and break_point != 0:
                break
            node = node.next

    def clean(self, asc):
        self.__init__(asc)

    def len(self):
        node = self.head
        count_node = 0
        while node is not None:
            count_node += 1
            node = node.next
        return count_node  # здесь будет ваш код

    def get_all(self):
        r = []
        node = self.head
        while node is not None:
            r.append(node)
            node = node.next
        return r


class OrderedStringList(OrderedList):
    def __init__(self, asc):
        super(OrderedStringList, self).__init__(asc)

    def compare(self, v1, v2):
        v1 = v1.lstrip().rstrip()
        v2 = v2.lstrip().rstrip()
        if v1 < v2:
            return -1  # -1 если v1 < v2
        elif v1 > v2:
            return 1  # +1 если v1 > v2
        else:
            return 0  # 0 если v1 == v2 # переопределённая версия для строк
    '''5. Переделайте функцию поиска элемента по значению 
    с учётом признака упорядоченности и возможности раннего прерывания поиска, 
    если найден заведомо больший или меньший элемент, нежели искомый. 
    Оцените сложность операции поиска, изменилась ли она?'''
    def find(self, val):
        node = self.head
        f_node = None
        if self.__ascending is True and self.compare(val, self.head.value) < 0:
            return None
        elif self.__ascending is False and self.compare(self.tail.value, val) < 0:
            return None
        else:
            while node is not None:
                if node.value == val:
                    f_node = node
                    break
                node = node.next
            return f_node
