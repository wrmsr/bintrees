#!/usr/bin/env python
#coding:utf-8
# Author:  mozman
# Purpose: cython unbalanced binary tree module
# Created: 28.04.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

from .abctree import ABCTree

from .cython_basetree cimport _BaseTree
from .ctrees cimport avl_insert, avl_remove

cdef class _AVLTree(_BaseTree):
    def insert(self, key, value):
        res = avl_insert(&self._root, key, value)
        if res < 0:
            raise MemoryError('Can not allocate memory for node structure.')
        else:
            self._count += res

    def remove(self, key):
        cdef int result
        result =  avl_remove(&self._root, key)
        if result == 0:
            raise KeyError(str(key))
        else:
            self._count -= 1

class FastAVLTree(_AVLTree, ABCTree):
    pass