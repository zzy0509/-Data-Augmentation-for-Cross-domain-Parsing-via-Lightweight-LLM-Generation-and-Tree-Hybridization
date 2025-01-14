# -*- coding=utf-8 -*-

import re

from nltk.tree import Tree

# split constituent label and head word
REP_NODE = re.compile(r'(.*)\[([0-9]+)\]')

class ConstituentTree(Tree):

    def __init__(self, node: str,
                 children: list = None,
                 sent_id: int = None,
                 replaceable: bool = True,
                 hybrid_level: int = 0,
                 top: bool = False):
        super().__init__(node, children=children)
        self._sent_id = sent_id
        self._replaceable = replaceable
        self._hybrid_level = hybrid_level
        self._top = top
        self._raw = False

    def sent_id(self):
        return self._sent_id

    def set_sent_id(self, id):
        self._sent_id = id

    def span(self):
        return self._span

    def set_span(self, span):
        self._span = span

    def replaceable(self):
        return self._replaceable

    def hybrid_level(self):
        # level = 1 if self._hybridized else 0
        # for child in self:
        #     if isinstance(child, Tree) and not isinstance(child[0], str):
        #         level += child.hybrid_level()
        return self._hybrid_level

    def top(self):
        """Whether a tree is a complete example, i.e. with `S` as the root."""
        return self._top

    def raw(self):
        """Generated or from treebank."""
        return self._raw

    def set_raw(self):
        self._raw = True

    def equal(self, tree):
        """Check whether two trees are the same."""
        # TODO
        if self.one_line() == tree.one_line():
            return True
        return False
    
    def equal_leaves(self, tree):
        if " ".join(self.leaves()) == " ".join(tree.leaves()):
            return True
        return False
    
    def equal_production(self, tree):
        """Check whether two trees are of the same production."""
        if not self.label_repr() == tree.label_repr():
            return False
        if not len(self) == len(tree):
            return False
        for i in range(len(self)):
            if not self[i].label() == tree[i].label():
                return False
        return True

    def update_position(self, ps, child):
        """Replace a child with via position."""
        self[ps] = child

    def update(self, idx: int, child):
        """Replace a child with a new one."""
        if idx >= len(self):
            raise IndexError
        self._hybrid_level += child.hybrid_level() - self[idx].hybrid_level()
        if child.sent_id() != self._sent_id:
            self._hybrid_level += 1
        self[idx] = child

    def node_size(self):
        n = 1
        for child in self:
            if isinstance(child, Tree) and not isinstance(child[0], str):
                n += child.node_size()
        return n

    def size(self):
        return len(self.leaves())
        # n = 1
        # for child in self:
        #     if isinstance(child, Tree) and not isinstance(child[0], str):
        #         n += child.size()
        # return n

    def label_repr(self):
        return self._label

    def __repr__(self):
        # TODO
        childstr = " ".join(repr(c) for c in self)
        return "({} {})".format(self.label_repr(), childstr)

    def one_line(self):
        # TODO
        """Display tree representation in one line, and head word is in the form of string or digit."""
        childstr = " ".join([c.one_line() if isinstance(c, Tree) else str(c) for c in self])
        return "({} {})".format(self.label_repr(), childstr)

    def tree_positions(self, order='preorder'):
        positions = []
        if order in ("preorder", "bothorder"):
            positions.append(())
        for i, child in enumerate(self):
            if isinstance(child, Tree) and not isinstance(child[0], str):
                childpos = child.tree_positions(order)
                positions.extend((i,) + p for p in childpos)
            # else:
            #     positions.append((i,))
        if order in ("postorder", "bothorder"):
            positions.append(())
        return positions

    def __copy__(self):
        return self.copy()

    def __deepcopy__(self, memo):
        return self.copy(deep=True)

    def copy(self, deep=False):
        if not deep:
            return type(self)(self._label, self, self._sent_id,
                              self._replaceable, self._hybrid_level, self._top)
        else:
            return type(self).convert(self)

    @classmethod
    def convert(cls, tree):
        """
        Convert a tree between different subtypes of Tree.  ``cls`` determines
        which class will be used to encode the new tree.

        :type tree: Tree
        :param tree: The tree that should be converted.
        :return: The new Tree.
        """
        # TODO no need copy children
        if isinstance(tree, Tree):
            children = [cls.convert(child) for child in tree]
            return cls(tree._label, children, tree._sent_id,
                       tree._replaceable, tree._hybrid_level, tree._top)
        else:
            return tree

    @classmethod
    def get_subtrees(cls, node: Tree):
        """
        Extract all non-terminals nodes from a Tree, POS nodes are not included.
        """
        subtrees = [node]
        for child in node:
            if isinstance(child, Tree) and not isinstance(child[0], str):
                subtrees.extend(cls.get_subtrees(child))
        return subtrees

    @classmethod
    def initialize(cls, tree: Tree, sent_id: int):
        """
        Obtain a ConstituentTree from a NLTK Tree.
        Spans start from 0 rather than 1.
        """
        words = tree.leaves()

        def track(tree: Tree, i: int, parent_repr: str, top: bool = False):
            """
            Args: 
                i (int): sentence id of this subtree
                parent_repr (str): `constituent label + head word`
                top (bool): whether the subtree is a full tree
            """
            if isinstance(tree, str):
                raise TypeError
            label = tree.label()
            # replaceable
            replaceable = True if label != parent_repr else False
            # end index and children node
            j, children = i, []
            # leaf POS node
            if isinstance(tree, Tree) and isinstance(tree[0], str):
                j = i + 1
                children.append(tree[0])
                replaceable = False
            # non-terminal
            else:
                for child in tree:
                    j, t = track(child, j, label)
                    children.append(t)

            t = ConstituentTree(label, children, sent_id, replaceable, 0, top)

            return j, t

        return track(tree, 0, '', True)[1]




