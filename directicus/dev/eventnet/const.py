"""
This module implements a form of constant, which can be shared safely across modules.
This module is not designed to be used using 'import * from const' syntax.
"""
class _ConstantCollection(object):
    def __init__(self):
        self.__dict__['_reverse'] = {}
        self.__dict__['constants'] = {}
    def __setattr__(self, key, value):
        raise Exception, 'Cannot assign to the Constant Collection. User register() instead.'

    def register(self, name, value=None):
        if name in self.__dict__:
            raise Exception, '%s is already defined as a constant.' % name
        if value is None:
            value = hash(name)
        if(value in self._reverse):
            lookup_name = self._reverse[value] + "|" + name
        else:
            lookup_name = name
        self.__dict__[name] = value
        self.constants[name] = value
        self._reverse[value] = lookup_name
        return value

    def lookup(self, value):
        try:
            return self._reverse[value]
        except KeyError:
            raise NameError, 'Uknown constant.'

import sys
sys.modules[__name__] = _ConstantCollection()

