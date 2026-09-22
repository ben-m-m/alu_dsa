import unittest
from data_structures.stack import Stack


class TestStack(unittest.TestCase):
    def test_new_stack_is_empty(self):
        stack = Stack()

        self.assertTrue(stack.is_empty())

    def test_push_adds_item(self):
        stack = Stack()
        stack.push(10)
        self.assertEqual(stack.size(), 1)

    def test_peek_returns_top_item(self):
        stack = Stack()

        stack.push(10)
        stack.push(20)

        self.assertEqual(stack.peek(), 20)
        self.assertEqual(stack.size(), 2)

    def test_pop_returns_top_item(self):
        stack = Stack()

        stack.push(10)
        stack.push(20)
        stack.push(30)

        self.assertEqual(stack.pop(), 30)

    def test_pop_removes_items(self):
        stack = Stack()

        stack.push(10)
        stack.push(20)
        stack.push(30)

        stack.pop()

        self.assertEqual(stack.size(), 2)
        self.assertEqual(stack.peek(), 20)

    def test_pop_empty_stack_raise_error(self):
        stack = Stack()

        with self.assertRaises(IndexError):
            stack.pop()

    def test_peek_empty_stack_raises_error(self):
        stack = Stack()

        with self.assertRaises(IndexError):
            stack.peek()

    def test_stack_is_empty_after_all_items_are_popped(self):
        stack = Stack()

        stack.push(10)
        stack.push(20)

        stack.pop()
        stack.pop()

        self.assertTrue(stack.is_empty())


if __name__ == "__main__":
    unittest.main()