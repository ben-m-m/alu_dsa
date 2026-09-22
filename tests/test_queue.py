import unittest
from data_structures.queue import Queue


class TestQueue(unittest.TestCase):
    def test_new_queue_is_empty(self):
        queue = Queue()

        self. assertTrue(queue.is_empty())


if __name__ == "__main__":
    unittest.main()
