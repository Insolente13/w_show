class Stack:
    def __init__(self):
        self.stack = []

    def size(self):
        return len(self.stack)

    def push(self, element):
        self.stack.insert(-1, element)

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
