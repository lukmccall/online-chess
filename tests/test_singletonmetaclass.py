from unittest import TestCase

from langextensions import SingletonMeta


class TestSingletonMeta(TestCase):
    def test_if_singleton_is_created(self):
        class TestClass(metaclass=SingletonMeta):
            pass

        self.assertTrue(callable(TestClass))
        singleton = TestClass()
        self.assertIs(singleton, TestClass())
