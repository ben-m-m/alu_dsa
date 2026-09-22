from collections import deque


class Queue:

    def __init__(self):
        self.items = deque()

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("cannot dequeu from an empty queue")
        return self.items.popleft()

    def front(self):
        if self.is_empty:
            raise IndexError("Cannot view the front of an empty queue")
        return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)