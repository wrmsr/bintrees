#!/usr/bin/env python
#coding:utf-8
# Author:  Mozman
# Purpose: abstract base class for all binary trees
# Created: 03.05.2010
# Copyright (c) 2010-2013 by Manfred Moitzi
# License: MIT License

from __future__ import absolute_import

from .treeslice import TreeSlice
from operator import attrgetter, lt, gt

class _ABCTree(object):
    """
    Abstract-Base-Class for the pure Python Trees: BinaryTree, AVLTree and RBTree

    The ABCTree Class
    =================

    T has to implement following properties
    ---------------------------------------

    count -- get node count

    T has to implement following methods
    ------------------------------------

    get_value(...)
        get_value(key) -> returns value for key

    insert(...)
        insert(key, value) <==> T[key] = value, insert key into T

    remove(...)
        remove(key) <==> del T[key], remove key from T

    clear(...)
        T.clear() -> None.  Remove all items from T.

    iter_items(...)
        iter_items(start_key, end_key, [reverse]) -> iterate over all items, yielding (k, v) tuple

    foreach(...)
        foreach(f, [order]) -> visit all nodes of tree and call f(k, v) for each node, O(n)

    pop_item(...)
        T.popitem() -> (k, v), remove and return some (key, value)

    min_item(...)
        min_item() -> get smallest (key, value) pair of T, O(log(n))

    max_item(...)
        max_item() -> get largest (key, value) pair of T, O(log(n))

    prev_item(...)
        prev_item(key) -> get (k, v) pair, where k is predecessor to key, O(log(n))

    succ_item(...)
        succ_item(key) -> get (k,v) pair as a 2-tuple, where k is successor to key, O(log(n))

    floor_item(...)
        floor_item(key) -> get (k, v) pair, where k is the greatest key less than or equal to key, O(log(n))

    ceiling_item(...)
        ceiling_item(key) -> get (k, v) pair, where k is the smallest key greater than or equal to key, O(log(n))

    Methods defined here
    --------------------

    * __contains__(k) -> True if T has a key k, else False, O(log(n))
    * __delitem__(y) <==> del T[y], del T[s:e], O(log(n))
    * __getitem__(y) <==> T[y], T[s:e], O(log(n))
    * __iter__() <==> iter(T)
    * __len__() <==> len(T), O(1)
    * __max__() <==> max(T), get max item (k,v) of T, O(log(n))
    * __min__() <==> min(T), get min item (k,v) of T, O(log(n))
    * __and__(other) <==> T & other, intersection
    * __or__(other) <==> T | other, union
    * __sub__(other) <==> T - other, difference
    * __xor__(other) <==> T ^ other, symmetric_difference
    * __repr__() <==> repr(T)
    * __setitem__(k, v) <==> T[k] = v, O(log(n))
    * clear() -> None, Remove all items from T, , O(n)
    * remove_items(keys) -> remove items by keys
    * copy() -> a shallow copy of T, O(n*log(n))
    * discard(k) -> None, remove k from T, if k is present, O(log(n))
    * get(k[,d]) -> T[k] if k in T, else d, O(log(n))
    * is_empty() -> True if len(T) == 0, O(1)
    * keys([reverse]) -> generator for keys of T, O(n)
    * values([reverse]) -> generator for values of  T, O(n)
    * pop(k[,d]) -> v, remove specified key and return the corresponding value, O(log(n))
    * set_default(k[,d]) -> T.get(k, d), also set T[k]=d if k not in T, O(log(n))
    * update(E) -> None.  Update T from dict/iterable E, O(E*log(n))

    slicing by keys

    * key_slice(s, e[, reverse]) -> generator for keys of T for s <= key < e, O(n)
    * value_slice(s, e[, reverse]) -> generator for values of T for s <= key < e, O(n)
    * item_slice(s, e[, reverse]) -> generator for items of T for s <= key < e, O(n)
    * T[s:e] -> TreeSlice object, with keys in range s <= key < e, O(n)
    * del T[s:e] -> remove items by key slicing, for s <= key < e, O(n)

    if 's' is None or T[:e] TreeSlice/iterator starts with value of min_key()
    if 'e' is None or T[s:] TreeSlice/iterator ends with value of max_key()
    T[:] is a TreeSlice which represents the whole tree.

    TreeSlice is a tree wrapper with range check, and contains no references
    to objects, deleting objects in the associated tree also deletes the object
    in the TreeSlice.

    * TreeSlice[k] -> get value for key k, raises KeyError if k not exists in range s:e
    * TreeSlice[s1:e1] -> TreeSlice object, with keys in range s1 <= key < e1

      * new lower bound is max(s, s1)
      * new upper bound is min(e, e1)

    TreeSlice methods:

    * items() -> generator for (k, v) items of T, O(n)
    * keys() -> generator for keys of T, O(n)
    * values() -> generator for values of  T, O(n)
    * __iter__ <==> keys()
    * __repr__ <==> repr(T)
    * __contains__(key)-> True if TreeSlice has a key k, else False, O(log(n))

    prev/succ operations

    * prev_key(key) -> k, get the predecessor of key, O(log(n))
    * succ_key(key) -> k, get the successor of key, O(log(n))
    * floor_key(key) -> k, get the greatest key less than or equal to key, O(log(n))
    * ceiling_key(key) -> k, get the smallest key greater than or equal to key, O(log(n))

    Heap methods

    * max_key() -> get largest key of T, O(log(n))
    * min_key() -> get smallest key of T, O(log(n))
    * pop_min() -> (k, v), remove item with minimum key, O(log(n))
    * pop_max() -> (k, v), remove item with maximum key, O(log(n))
    * nlargest(i[,pop]) -> get list of i largest items (k, v), O(i*log(n))
    * nsmallest(i[,pop]) -> get list of i smallest items (k, v), O(i*log(n))

    Set methods (using frozenset)

    * intersection(t1, t2, ...) -> Tree with keys *common* to all trees
    * union(t1, t2, ...) -> Tree with keys from *either* trees
    * difference(t1, t2, ...) -> Tree with keys in T but not any of t1, t2, ...
    * symmetric_difference(t1) -> Tree with keys in either T and t1  but not both
    * is_subset(S) -> True if every element in T is in S
    * is_superset(S) -> True if every element in S is in T
    * is_disjoint(S) ->  True if T has a null intersection with S

    Classmethods

    * from_keys(S[,v]) -> New tree with keys from S and values equal to v.

    """

    def __repr__(self):
        """ x.__repr__(...) <==> repr(x) """
        tpl = "%s({%s})" % (self.__class__.__name__, '%s')
        return tpl % ", ".join( ("%r: %r" % item for item in self.items()) )

    def copy(self):
        """ T.copy() -> get a shallow copy of T. """
        tree = self.__class__()
        self.foreach(tree.insert, order=-1)
        return tree
    __copy__ = copy

    def __contains__(self, key):
        """ k in T -> True if T has a key k, else False """
        try:
            self.get_value(key)
            return True
        except KeyError:
            return False

    def __len__(self):
        """ x.__len__() <==> len(x) """
        return self.count

    def __min__(self):
        """ x.__min__() <==> min(x) """
        return self.min_item()

    def __max__(self):
        """ x.__max__() <==> max(x) """
        return self.max_item()

    def __and__(self, other):
        """ x.__and__(other) <==> self & other """
        return self.intersection(other)

    def __or__(self, other):
        """ x.__or__(other) <==> self | other """
        return self.union(other)

    def __sub__(self, other):
        """ x.__sub__(other) <==> self - other """
        return self.difference(other)

    def __xor__(self, other):
        """ x.__xor__(other) <==> self ^ other """
        return self.symmetric_difference(other)

    def discard(self, key):
        """ x.discard(k) -> None, remove k from T, if k is present """
        try:
            self.remove(key)
        except KeyError:
            pass

    def __del__(self):
        self.clear()

    def is_empty(self):
        """ x.is_empty() -> False if T contains any items else True"""
        return self.count == 0

    def keys(self, reverse=False):
        """ T.iterkeys([reverse]) -> an iterator over the keys of T, in ascending
        order if reverse is True, iterate in descending order, reverse defaults
        to False
        """
        return (item[0] for item in self.iter_items(reverse=reverse))
    __iter__ = keys

    def __reversed__(self):
        return self.keys(reverse=True)

    def values(self, reverse=False):
        """ T.values([reverse]) -> an iterator over the values of T, in ascending order
        if reverse is True, iterate in descending order, reverse defaults to False
        """
        return (item[1] for item in self.iter_items(reverse=reverse))

    def items(self, reverse=False):
        """ T.items([reverse]) -> an iterator over the (key, value) items of T,
        in ascending order if reverse is True, iterate in descending order,
        reverse defaults to False
        """
        return self.iter_items(reverse=reverse)

    def __getitem__(self, key):
        """ x.__getitem__(y) <==> x[y] """
        if isinstance(key, slice):
            return TreeSlice(self, key.start, key.stop)
        else:
            return self.get_value(key)

    def __setitem__(self, key, value):
        """ x.__setitem__(i, y) <==> x[i]=y """
        if isinstance(key, slice):
            raise ValueError('setslice is not supported')
        self.insert(key, value)

    def __delitem__(self, key):
        """ x.__delitem__(y) <==> del x[y] """
        if isinstance(key, slice):
            self.remove_items(self.keyslice(key.start, key.stop))
        else:
            self.remove(key)

    def remove_items(self, keys):
        """ T.remove_items(keys) -> remove items by keys
        """
        # convert generator to a set, because the content of the
        # tree will be modified!
        for key in frozenset(keys):
            self.remove(key)

    def key_slice(self, start_key, end_key, reverse=False):
        """ T.key_slice(start_key, end_key) -> key iterator:
        start_key <= key < end_key.

        Yields keys in ascending order if reverse is False else in descending order.
        """
        return (k for k, v in self.iter_items(start_key, end_key, reverse=reverse))
    keyslice = key_slice  # for compatibility

    def value_slice(self, start_key, end_key, reverse=False):
        """ T.value_slice(start_key, end_key) -> value iterator:
        start_key <= key < end_key.

        Yields values in ascending key order if reverse is False else in descending key order.
        """
        return (v for k, v in self.iter_items(start_key, end_key, reverse=reverse))
    valueslice = value_slice  # for compatibility

    def item_slice(self, start_key, end_key, reverse=False):
        """ T.item_slice(start_key, end_key) -> item iterator:
        start_key <= key < end_key.

        Yields items in ascending key order if reverse is False else in descending key order.
        """
        return self.iter_items(start_key, end_key, reverse)

    def __getstate__(self):
        return dict(self.items())

    def __setstate__(self, state):
        # note for myself: this is called like __init__, so don't use clear()
        # to remove existing data!
        self._root = None
        self._count = 0
        self.update(state)

    def set_default(self, key, default=None):
        """ T.setdefault(k[,d]) -> T.get(k,d), also set T[k]=d if k not in T """
        try:
            return self.get_value(key)
        except KeyError:
            self.insert(key, default)
            return default
    setdefault = set_default  # for compatibility

    def update(self, *args):
        """ T.update(E) -> None. Update T from E : for (k, v) in E: T[k] = v """
        for items in args:
            try:
                generator = items.items()
            except AttributeError:
                generator = iter(items)

            for key, value in generator:
                self.insert(key, value)

    @classmethod
    def from_keys(cls, iterable, value=None):
        """ T.fromkeys(S[,v]) -> New tree with keys from S and values equal to v.

        v defaults to None.
        """
        tree = cls()
        for key in iterable:
            tree.insert(key, value)
        return tree
    fromkeys = from_keys  # for compatibility

    def get(self, key, default=None):
        """ T.get(k[,d]) -> T[k] if k in T, else d.  d defaults to None. """
        try:
            return self.get_value(key)
        except KeyError:
            return default

    def pop(self, key, *args):
        """ T.pop(k[,d]) -> v, remove specified key and return the corresponding value
        If key is not found, d is returned if given, otherwise KeyError is raised
        """
        if len(args) > 1:
            raise TypeError("pop expected at most 2 arguments, got %d" % (1 + len(args)))
        try:
            value = self.get_value(key)
            self.remove(key)
            return value
        except KeyError:
            if len(args) == 0:
                raise
            else:
                return args[0]

    def prev_key(self, key):
        """ Get predecessor to key, raises KeyError if key is min key
        or key does not exist.
        """
        return self.prev_item(key)[0]

    def succ_key(self, key):
        """ Get successor to key, raises KeyError if key is max key
        or key does not exist.
        """
        return self.succ_item(key)[0]

    def floor_key(self, key):
        """ Get the greatest key less than or equal to the given key, raises
        KeyError if there is no such key.
        """
        return self.floor_item(key)[0]

    def ceiling_key(self, key):
        """ Get the smallest key greater than or equal to the given key, raises
        KeyError if there is no such key.
        """
        return self.ceiling_item(key)[0]

    def pop_min(self):
        """ T.pop_min() -> (k, v), remove item with minimum key, raise ValueError
        if T is empty.
        """
        item = self.min_item()
        self.remove(item[0])
        return item

    def pop_max(self):
        """ T.pop_max() -> (k, v), remove item with maximum key, raise ValueError
        if T is empty.
        """
        item = self.max_item()
        self.remove(item[0])
        return item

    def min_key(self):
        """ Get min key of tree, raises ValueError if tree is empty. """
        return  self.min_item()[0]

    def max_key(self):
        """ Get max key of tree, raises ValueError if tree is empty. """
        return self.max_item()[0]

    def nsmallest(self, n, pop=False):
        """ T.nsmallest(n) -> get list of n smallest items (k, v).
        If pop is True, remove items from T.
        """
        if pop:
            return [self.pop_min() for _ in range(min(len(self), n))]
        else:
            items = self.items()
            return [next(items) for _ in range(min(len(self), n))]

    def nlargest(self, n, pop=False):
        """ T.nlargest(n) -> get list of n largest items (k, v).
        If pop is True remove items from T.
        """
        if pop:
            return [self.pop_max() for _ in range(min(len(self), n))]
        else:
            items = self.items(reverse=True)
            return [next(items) for _ in range(min(len(self), n))]

    def intersection(self, *trees):
        """ x.intersection(t1, t2, ...) -> Tree, with keys *common* to all trees
        """
        thiskeys = frozenset(self.keys())
        sets = _build_sets(trees)
        rkeys = thiskeys.intersection(*sets)
        return self.__class__(((key, self.get(key)) for key in rkeys))

    def union(self, *trees):
        """ x.union(t1, t2, ...) -> Tree with keys from *either* trees
        """
        thiskeys = frozenset(self.keys())
        rkeys = thiskeys.union(*_build_sets(trees))
        all_trees = [self]
        all_trees.extend(trees)
        return self.__class__(((key, _multi_tree_get(all_trees, key)) for key in rkeys))

    def difference(self, *trees):
        """ x.difference(t1, t2, ...) -> Tree with keys in T but not any of t1,
        t2, ...
        """
        thiskeys = frozenset(self.keys())
        rkeys = thiskeys.difference(*_build_sets(trees))
        return self.__class__(((key, self.get(key)) for key in rkeys))

    def symmetric_difference(self, tree):
        """ x.symmetric_difference(t1) -> Tree with keys in either T and t1  but
        not both
        """
        thiskeys = frozenset(self.keys())
        rkeys = thiskeys.symmetric_difference(frozenset(tree.keys()))
        all_trees = [self, tree]
        return self.__class__(((key, _multi_tree_get(all_trees, key)) for key in rkeys))

    def is_subset(self, tree):
        """ x.issubset(tree) -> True if every element in x is in tree """
        thiskeys = frozenset(self.keys())
        return thiskeys.issubset(frozenset(tree.keys()))
    issubset = is_subset  # for compatibility

    def is_superset(self, tree):
        """ x.issubset(tree) -> True if every element in tree is in x """
        thiskeys = frozenset(self.keys())
        return thiskeys.issuperset(frozenset(tree.keys()))
    issuperset = is_superset  # for compatibility

    def is_disjoint(self, tree):
        """ x.isdisjoint(S) ->  True if x has a null intersection with tree """
        thiskeys = frozenset(self.keys())
        return thiskeys.isdisjoint(frozenset(tree.keys()))
    isdisjoint = is_disjoint  # for compatibility


def _build_sets(trees):
    return [frozenset(tree.keys()) for tree in trees]


def _multi_tree_get(trees, key):
    for tree in trees:
        try:
            return tree[key]
        except KeyError:
            pass
    raise KeyError(key)


class ABCTree(_ABCTree):
    """ Base class for the pure Python implementation of trees.

    T has to implement following properties
    ---------------------------------------

    count -- get node count
    root -- get root node

    T has to implement following methods
    ------------------------------------

    insert(...)
        insert(key, value) <==> T[key] = value, insert key into T

    remove(...)
        remove(key) <==> del T[key], remove key from T

    clear(...)
        T.clear() -> None.  Remove all items from T.

    Methods defined here
    --------------------

    * get_value(key) -> returns value for key
    * items([reverse]) -> iterate over all items, yielding (k, v) tuple
    * item_slice(start_key, end_key, [reverse]) -> iterate over all items, yielding (k, v) tuple
    * foreach(f, [order]) -> visit all nodes of tree and call f(k, v) for each node, O(n)
    * popitem() -> (k, v), remove and return some (key, value)
    * min_item() -> get smallest (key, value) pair of T, O(log(n))
    * max_item() -> get largest (key, value) pair of T, O(log(n))
    * prev_item(key) -> get (k, v) pair, where k is predecessor to key, O(log(n))
    * succ_item(key) -> get (k,v) pair as a 2-tuple, where k is successor to key, O(log(n))
    * floor_item(key) -> get (k, v) pair, where k is the greatest key less than or equal to key, O(log(n))
    * ceiling_item(key) -> get (k, v) pair, where k is the smallest key greater than or equal to key, O(log(n))

    """
    def get_value(self, key):
        node = self._root
        while node is not None:
            if key == node.key:
                return node.value
            elif key < node.key:
                node = node.left
            else:
                node = node.right
        raise KeyError(str(key))

    def pop_item(self):
        """ T.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if T is empty
        """
        if self.is_empty():
            raise KeyError("popitem(): tree is empty")
        node = self._root
        while True:
            if node.left is not None:
                node = node.left
            elif node.right is not None:
                node = node.right
            else:
                break
        key = node.key
        value = node.value
        self.remove(key)
        return key, value
    popitem = pop_item  # for compatibility

    def foreach(self, func, order=0):
        """ Visit all tree nodes and process key, value.

        parm func: function(key, value)
        param int order: inorder = 0, preorder = -1, postorder = +1

        """
        def _traverse(node):
            if order == -1:
                func(node.key, node.value)
            if node.left is not None:
                _traverse(node.left)
            if order == 0:
                func(node.key, node.value)
            if node.right is not None:
                _traverse(node.right)
            if order == +1:
                func(node.key, node.value)
        _traverse(self._root)

    def min_item(self):
        """ Get item with min key of tree, raises ValueError if tree is empty. """
        if self.count == 0:
            raise ValueError("Tree is empty")
        node = self._root
        while node.left is not None:
            node = node.left
        return node.key, node.value

    def max_item(self):
        """ Get item with max key of tree, raises ValueError if tree is empty. """
        if self.count == 0:
            raise ValueError("Tree is empty")
        node = self._root
        while node.right is not None:
            node = node.right
        return node.key, node.value

    def _next_item(self, key, left, right, less_than):
        node = self._root
        succ = None
        while node is not None:
            if key == node.key:
                break
            elif less_than(key, node.key):
                if (succ is None) or less_than(node.key, succ.key):
                    succ = node
                node = left(node)
            else:
                node = right(node)

        if node is None:  # stay at dead end
            raise KeyError(str(key))
        # found node of key
        if right(node) is not None:
            # find smallest node of right subtree
            node = right(node)
            while left(node) is not None:
                node = left(node)
            if succ is None:
                succ = node
            elif less_than(node.key, succ.key):
                succ = node
        elif succ is None:  # given key is biggest in tree
            raise KeyError(str(key))
        return succ.key, succ.value

    def succ_item(self, key):
        """ Get successor (k,v) pair of key, raises KeyError if key is max key
        or key does not exist.
        """
        if self.count == 0:
            raise KeyError("Tree is empty")
        return self._next_item(
            key,
            left=attrgetter("left"),
            right=attrgetter("right"),
            less_than=lt,
        )

    def prev_item(self, key):
        """ Get predecessor (k,v) pair of key, raises KeyError if key is min key
        or key does not exist.
        """
        if self.count == 0:
            raise KeyError("Tree is empty")
        return self._next_item(
            key,
            left=attrgetter("right"),
            right=attrgetter("left"),
            less_than=gt,
        )

    def floor_item(self, key):
        """ Get the element (k,v) pair associated with the greatest key less
        than or equal to the given key, raises KeyError if there is no such key.
        """
        node = self._root
        prev = None
        while node is not None:
            if key == node.key:
                return node.key, node.value
            elif key < node.key:
                node = node.left
            else:
                if (prev is None) or (node.key > prev.key):
                    prev = node
                node = node.right
        # node must be None here
        if prev:
            return prev.key, prev.value
        raise KeyError(str(key))

    def ceiling_item(self, key):
        """ Get the element (k,v) pair associated with the smallest key greater
        than or equal to the given key, raises KeyError if there is no such key.
        """
        node = self._root
        succ = None
        while node is not None:
            if key == node.key:
                return node.key, node.value
            elif key > node.key:
                node = node.right
            else:
                if (succ is None) or (node.key < succ.key):
                    succ = node
                node = node.left
            # node must be None here
        if succ:
            return succ.key, succ.value
        raise KeyError(str(key))

    def iter_items(self,  start_key=None, end_key=None, reverse=False):
        if self.is_empty():
            return []
        if reverse:
            return self.iter_items_backward(start_key, end_key)
        else:
            return self.iter_items_forward(start_key, end_key)

    def iter_items_forward(self, start_key=None, end_key=None):
        for item in self._iter_items(left=attrgetter("left"), right=attrgetter("right"),
                                     start_key=start_key, end_key=end_key):
            yield item

    def iter_items_backward(self, start_key=None, end_key=None):
        for item in self._iter_items(left=attrgetter("right"), right=attrgetter("left"),
                                     start_key=start_key, end_key=end_key):
            yield item

    def _iter_items(self, left=attrgetter("left"), right=attrgetter("right"), start_key=None, end_key=None):
        """Iterates over the (key, value) items of the associated tree,
        in ascending order if reverse is True, iterate in descending order,
        reverse defaults to False

        optimized iterator (reduced method calls)
        """
        if self.is_empty():
            return

        if start_key is None and end_key is None:
            in_range = lambda x: True
        else:
            if start_key is None:
                start_key = self.min_key()
            if end_key is None:
                in_range = lambda x: x >= start_key
            else:
                in_range = lambda x: start_key <= x < end_key

        node = self._root
        stack = []
        go_left = True
        while True:
            if left(node) is not None and go_left:
                stack.append(node)
                node = left(node)
            else:
                if in_range(node.key):
                    yield node.key, node.value
                if right(node) is not None:
                    node = right(node)
                    go_left = True
                else:
                    if not len(stack):
                        return  # all done
                    node = stack.pop()
                    go_left = False

