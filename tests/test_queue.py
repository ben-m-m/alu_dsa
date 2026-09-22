import unittest
from data_structures.queue import Queue


class TestQueue(unittest.TestCase):
    def test_new_queue_is_empty(self):
        queue = Queue()

        self. assertTrue(queue.is_empty())

    def test_enque_adds_items(self):
        queue = Queue()
        queue.enqueue(10)

        self.assertEqual(queue.size(), 1)

    def test_front_returns_first_item(self):
        queue = Queue()

        queue.enqueue(10)
        queue.enqueue(20)
        queue.enqueue(30)

        self.assertEqual(queue.front(), 10)
        self.assertEqual(queue.size(), 3)

    def test_dequeue_returns_first_item(self):
        queue = Queue()

        queue.enqueue(10)
        queue.enqueue(20)
        queue.enqueue(30)

        self.assertEqual(queue.dequeue(), 10)

    def test_dequeue_removes_first_item(self):
        queue = Queue()

        queue.enqueue(10)
        queue.enqueue(20)
        queue.enqueue(30)

        queue.dequeue()

        self.assertEqual(queue.size(), 2)
        self.assertEqual(queue.front(), 20)

    def test_dequeue_empty_queue_raises_error(self):
        queue = Queue()

        with self.assertRaises(IndexError):
            queue.dequeue()

    def test_front_empty_queue_raises_error(self):
        queue = Queue()

        with self.assertRaises(IndexError):
            queue.front()

    def test_queue_is_empty_after_all_items_are_dequeued(self):
        queue = Queue()

        queue.enqueue(10)
        queue.enqueue(20)

        queue.dequeue()
        queue.dequeue()

        self.assertTrue(queue.is_empty())


if __name__ == "__main__":
    unittest.main()
