# -*- coding=utf-8 -*-

from lexical_tree import LexTree

from nltk.tree import Tree


class TreeDataset(object):
    """One level tree dataset"""

    def __init__(self, trees, dataset) -> None:
        self.trees = trees
        self.dataset = dataset

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        if idx >= len(self.dataset):
            raise IndexError
        return self.dataset[idx]

    def size(self) -> int:
        return len(self.dataset)

    def add(self, tree: Tree) -> None:
        self.dataset.append(tree)

    @classmethod
    def build(cls, src: str):
        with open(src, 'r', encoding='utf-8') as fr:
            trees = [Tree.fromstring(line)[0] for line in fr]
        trees = [LexTree.const2lex(t, i) for i, t in enumerate(trees)]
        for tree in trees:
            tree.set_raw()
        return cls(trees, trees)

    def count_sizes(self):
        print('total elements of dataset: {}'.format(self.size()))


class HierarchicalDataset(object):

    def __init__(self, trees, dataset) -> None:
        self.trees = trees
        self.dataset = dataset

    def __getitem__(self, idx):
        if self.dataset.get(idx, None) is None:
            raise KeyError
        return self.dataset[idx]

    def size(self) -> int:
        return sum([len(self.dataset[level]) for level in self.hierarchy()])

    def add(self, tree: Tree, level: int) -> None:
        self.dataset[level].append(tree)

    @classmethod
    def hierarchy(cls):
        return [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    @classmethod
    def hierarchy_split(cls, size):
        if size <= 5:
            return 1
        elif size > 5 and size <= 10:
            return 2
        elif size > 10 and size <= 15:
            return 3
        elif size > 15 and size <= 20:
            return 4
        elif size > 20 and size <= 25:
            return 5
        elif size > 25 and size <= 30:
            return 6
        elif size > 30 and size <= 40:
            return 7
        elif size > 40 and size <= 50:
            return 8
        elif size > 50:
            return 9



    @classmethod
    def build(cls, src: str):
        with open(src, 'r', encoding='utf-8') as fr:
            trees = [Tree.fromstring(line) for line in fr]
        trees = [LexTree.const2lex(t, i) for i, t in enumerate(trees)]
        unique_set = set()
        dataset = dict()
        # TODO top level
        tops = []
        for h in cls.hierarchy():
            dataset[h] = []
        for tree in trees:
            subtrees = LexTree.get_subtrees(tree)
            for subtree in subtrees:
                subtree.set_raw()
            # if 'TOP' in subtrees[0].label():
            #     tops.append(subtrees[0])
            tops.append(subtrees[0])
            for subtree in subtrees[1:]:
                # if not subtree.replaceable():
                #     continue
                tree_repr = subtree.one_line()
                if tree_repr in unique_set:
                    continue
                unique_set.add(tree_repr)
                h = cls.hierarchy_split(subtree.size())
                dataset[h].append(subtree)
        dataset[cls.hierarchy()[-1]] = tops
        return cls(trees, dataset)
    
    @classmethod
    def build_and_add(cls, src1: str, src2: str):
        # print(src2,type(src2))
        with open(src1, 'r', encoding='utf-8') as fr1:
            trees1 = [Tree.fromstring(line)[0] for line in fr1]
        with open(src2, 'r', encoding='utf-8') as fr2:
            trees2 = [Tree.fromstring(line) for line in fr2]
        trees = trees1 + trees2
        trees = [LexTree.const2lex(t, i) for i, t in enumerate(trees)]
        # print(type(trees))
        # print(type(trees[0]))
        unique_set = set()
        dataset = dict()
        # TODO top level
        tops = []
        for h in cls.hierarchy():
            dataset[h] = []
        for tree in trees:
            # print(tree.one_line())
            subtrees = LexTree.get_subtrees(tree)
            for subtree in subtrees:
                # print(subtree)
                subtree.set_raw()
            tops.append(subtrees[0])
            for subtree in subtrees[1:]:
                # if not subtree.replaceable():
                #     continue
                # print(subtree)
                tree_repr = subtree.one_line()
                if tree_repr in unique_set:
                    continue
                unique_set.add(tree_repr)
                h = cls.hierarchy_split(subtree.size())
                dataset[h].append(subtree)
        dataset[cls.hierarchy()[-1]] = tops
        return cls(trees, dataset)
    

    def count_sizes(self):
        print('-------------------------------------')
        print('hierarchy dataset size statistic:')
        print('total elements: {}'.format(self.size()))
        for level in self.hierarchy():
            print("level {} of size: {}".format(level, len(self.dataset[level])))



