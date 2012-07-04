#! /usr/bin/env python
# ______________________________________________________________________
'''test_type_inference

Test type inference.
'''
# ______________________________________________________________________

from numba.minivect import minitypes
from numba import *
from numba import _numba_types as numba_types
from numba import ast_type_inference
from numba import decorators

import unittest

import numpy

# ______________________________________________________________________

def _simple_func(arg):
    if arg > 0.:
        result = 22.
    else:
        result = 42.
    return result

simple_func = decorators.function(_simple_func)

def _for_loop(start, stop, inc):
    acc = 0
    for value in range(start, stop, inc):
        acc += value
    return acc

for_loop = decorators.function(_for_loop)

def test_arange():
    a = numpy.arange(10)
    b = numpy.arange(10, dtype=numpy.double)
    return a, b

def test_empty_like(a):
    b = numpy.empty_like(a)
    c = numpy.zeros_like(a, dtype=numpy.int32)
    d = numpy.ones_like(a)

# ______________________________________________________________________

def infer(func, arg_types):
    sig = minitypes.FunctionType(return_type=None, args=arg_types)
    ast = decorators._get_ast(func)
    return ast_type_inference._infer_types(decorators.context, func, ast, sig)

class TestTypeInference(unittest.TestCase):
    # def test_simple_func(self):
    #     self.assertEqual(simple_func(-1.), 42.)
    #     self.assertEqual(simple_func(1.), 22.)

    # def test_simple_for(self):
    #     self.assertEqual(for_loop(0, 10, 1), 45)

    def test_type_infer_simple_func(self):
        sig, symtab = infer(_simple_func, [double])
        self.assertEqual(sig.return_type, double)

    def test_type_infer_for_loop(self):
        sig, symtab = infer(_for_loop, [int_, int_, int_])
        self.assertEqual(symtab['acc'].type, int_)
        self.assertEqual(symtab['value'].type, Py_ssize_t)
        self.assertEqual(sig.return_type, int_)

    def test_type_infer_arange(self):
        sig, symtab = infer(test_arange, [])
        self.assertEqual(symtab['a'].type, int64[:])
        self.assertEqual(symtab['b'].type, double[:])

    def test_empty_like(self):
        sig, symtab = infer(test_empty_like, [double[:]])
        self.assertEqual(symtab['b'].type, double[:])
        self.assertEqual(symtab['c'].type, int32[:])
        self.assertEqual(symtab['d'].type, double[:])

# ______________________________________________________________________

if __name__ == "__main__":
    #import dis
    # dis.dis(_simple_func)
    #dis.dis(for_loop)
    TestTypeInference('test_empty_like').debug()
    #unittest.main()