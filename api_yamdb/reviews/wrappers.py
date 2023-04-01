import inspect
import pprint


def print_args(func):
    def wrapper(*args, **kwargs):
        sig = inspect.signature(func)
        arg_names = list(sig.parameters.keys())
        print("arg_names", arg_names)
        for name, value in zip(arg_names, args):
            value = value.__dict__
            print(f"----{name}----")
            pprint.pprint(value)
        for name, value in kwargs.items():
            print(f"{name}: {value}")
        return func(*args, **kwargs)

    return wrapper
