from unittest import TestCase

from langextensions import abstract, Interface


class Test(TestCase):
    def test_abstract(self):
        @abstract
        def test_function():
            pass

        self.assertTrue(hasattr(test_function, "__isabstract__"))
        self.assertTrue(test_function.__isabstract__)


class TestInterface(TestCase):
    def test_if_interface_is_safe(self):
        class InnerInterface(metaclass=Interface):
            @abstract
            def need_to_be_implemented(self):
                pass

            def not_need_to_be_implemented(self):
                pass

        try:
            class IncorrectImplementation(InnerInterface):
                pass
            self.fail()
        except TypeError:
            pass

        try:
            class CorrectImplementation(InnerInterface):
                def need_to_be_implemented(self):
                    pass

            correct_object = CorrectImplementation()
            self.assertTrue(hasattr(correct_object, "not_need_to_be_implemented"))
        except TypeError:
            self.fail()
