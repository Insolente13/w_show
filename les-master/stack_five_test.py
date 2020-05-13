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


def five(brackets):
    brackets_stack = Stack()

    for x in range(len(brackets)):
        if brackets[x] == '(':
            brackets_stack.push(brackets[x])
        elif brackets[x] == ')':
            if brackets_stack.size() == 0:
                print('Не сбалансированы')
                break
            else:
                brackets_stack.pop()

    if brackets_stack.size() == 0:
        print('Cбалансированы')
    else:
        print('Не сбалансированы')


five('())))')
