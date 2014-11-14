#!/usr/bin/env python3
import collections
import types


# Constants
# VARS = {var_name, producer}
VARS = {}


def indent(text, prefix):
    newtext = ''
    for line in text.splitlines(True):
        newtext += '%s%s' % (prefix, line)
    return newtext


def _print_run(function):
    def wrapper(*args, **kwds):
        instance = args[0]
        if not instance.___printed___:
            print(instance)
            instance.___printed___ = True
        return function(*args, **kwds)
    return wrapper


def _capture_output(function):
    def wrapper(*args, **kwds):
        instance = args[0]
        out = function(*args, **kwds)
        if out is None:
            return

        annotation = function.__annotations__
        if 'return' in annotation:
            ret_types = annotation['return']
            if not isinstance(ret_types, collections.Iterable):
                VARS[id(out)] = instance
            else:
                for el in out:
                    VARS[id(el)] = instance
        return out
    return wrapper


class Printer(type):
    def __new__(cls, name, bases, dct):
        if 'run' in dct and isinstance(dct['run'], types.FunctionType):
            dct['run'] = _print_run(_capture_output(dct['run']))
            dct['___printed___'] = False
        return type.__new__(cls, name, bases, dct)


def printer(cls):
    if hasattr(cls, 'run'):
        m = getattr(cls, 'run')
        if isinstance(m, types.MethodType):
            setattr(cls, 'run', _print_run(m))
    return cls


# @printer
class Task(object, metaclass=Printer):
    # __metaclass__ = Printer

    def __init__(self, parent=None, skip=False, **kwds):
        self._indent = 0
        if parent is not None:
            self._indent += 4
        self._prefix = ' ' * self._indent

        self.skip = skip
        self.parent = parent
        self._kwds = kwds
        for kwd, val in list(kwds.items()):
            setattr(self, kwd, val)
        return

    def run(self, *args) -> None:
        self.input = args
        return

    # def __str__(self):
    #     return unicode(self).encode('utf-8')

    def __str__(self):
        u = 'task %s' % (self.__class__.__name__.lower())

        return indent(u, self._prefix)


class CompositeTask(object):
    pass


def timerange(start, end, step, relative=True):
    pass


class F1(Task):
    _indent = 0

    class T1(Task):
        def run(self) -> list:
            super(self.__class__, self).run()
            return list(range(100))

    class T2(Task):
        def run(self, input) -> [int, int]:
            super(self.__class__, self).run(input)
            return (1, 2)

    class T3(Task):
        def run(self, input) -> int:
            super(self.__class__, self).run(input)
            return 3

    class T4(Task):
        pass

    class T5(Task):
        pass

    class T6(Task):
        pass

    class T7(Task):
        pass

    def run(self, input=None, sleep=5):
        t1 = self.T1(parent=self)
        products = t1.run()

        (data1, data2) = self.T2(parent=self, sleep=3).run(products)
        data3 = self.T3(parent=self).run(data1)
        if data2:
            skip = True
        self.T4(parent=self, skip=skip).run(data1, data2)
        self.T5(parent=self).run(products[:30])
        self.T6(parent=self).run(products[:60])
        self.T7(parent=self).run(products[:90])
        return data3


# class F2(CompositeTask):
#     def run(self, input, sleep=5):
#         for t in timerange(0, 2, 1, relative=True):
#             self.T1(parent=self).run()
#         self.T2(parent=self).run(input)
#         return


def main():
    f1 = F1()
    # f2 = F2()

    data = f1.run()
    # f2.run(input=data)
    return data


if __name__ == '__main__':
    main()
