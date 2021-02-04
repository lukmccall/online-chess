def abstract(func):
    func.__isabstract__ = True
    return func


def rise_error(name, method, base):
    err_str = \
        """Can't create abstract class {name}! 
{name} must implement abstract method {method} of class {base_class}!""" \
            .format(name=name,
                    method=method,
                    base_class=base.__name__)
    raise TypeError(err_str)


class Interface(type):
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
        cls = super().__new__(cls, name, bases, namespace)
        return cls

    @staticmethod
    def _get_abstract_methods(namespace):
        return [
            name for name, val in namespace.items()
            if callable(val) and getattr(val, '__isabstract__', False)
        ]

    @staticmethod
    def _get_all_methods(namespace):
        return [name for name, val in namespace.items() if callable(val)]
