"""
A module that contains Interface extension for python
"""
from typing import Any, Callable, TypeVar, List

GenericFuncType = TypeVar('GenericFuncType', bound=Callable[..., Any])


def rise_error(name: str, method: str, base: Any):
    """Raises an error if method is not implemented

    :param name: Class name
    :param method: Method name
    :param base: Base class
    """
    # pylint: disable=C0303
    err_str = """Can't create abstract class {name}!  
    {name} must implement abstract method {method} of class {base_class}!""" \
        .format(name=name,
                method=method,
                base_class=base.__name__)
    raise TypeError(err_str)


def abstract(func: GenericFuncType):
    """A function decorator which mark method as abstract
    """
    func.__isabstract__ = True
    return func


class Interface(type):
    """
    Metaclass which simulated interface behaviour from other language
    """
    # noinspection PyMissingConstructor
    def __init__(cls, name, bases, _):  # pylint: disable=W0231
        for base in bases:
            must_implement = getattr(base, 'abstract_methods', [])
            class_methods = getattr(cls, 'all_methods', [])
            for method in must_implement:
                if method not in class_methods:
                    rise_error(name, method, base)

    # noinspection PyMethodParameters
    def __new__(cls, name, bases, namespace):
        namespace['abstract_methods'] = Interface._get_abstract_methods(namespace)
        namespace['all_methods'] = Interface._get_all_methods(namespace)
        cls = super().__new__(cls, name, bases, namespace)  # pylint: disable=W0642
        return cls

    @staticmethod
    def _get_abstract_methods(namespace: Any) -> List[GenericFuncType]:
        """Returns abstract methods from class

        :param namespace: Class
        :return: List of abstract methods
        """
        return [
            name for name, val in namespace.items()
            if callable(val) and getattr(val, '__isabstract__', False)
        ]

    @staticmethod
    def _get_all_methods(namespace: Any) -> List[GenericFuncType]:
        """Returns all methods

        :param namespace: Class
        :return: List of methods
        """
        return [name for name, val in namespace.items() if callable(val)]
