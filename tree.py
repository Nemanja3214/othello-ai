class TreeNode(object):
    __slots__ = '_parent', '_children', '_data', '_comparison_data'

    def __init__(self, data, comparison_data):
        self._parent = None
        self._children = []
        self._data = data
        self._comparison_data = comparison_data


    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, value):
        self._parent = value

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    @property
    def comparison_data(self):
        return self._comparison_data

    @comparison_data.setter
    def comparison_data(self, value):
        self._comparison_data = value

    def is_root(self):
        return self.parent is None

    def is_leaf(self):
        return len(self.children) == 0

    def add_child(self, x):
        # kreiranje dvosmerne veze između čvorova
        x.parent = self
        self.children.append(x)

    def __str__(self, level=0):
        ret = "\t" * level + str(self.data) + "\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def __lt__(self, other):
        return self.comparison_data < other.comparison_data

    def __le__(self, other):
        return self.comparison_data <= other.comparison_data

    def __gt__(self, other):
        return self.comparison_data > other.comparison_data

    def __ge__(self, other):
        return self.comparison_data >= other.comparison_data

    def has_children(self):
        return len(self.children) != 0


class Tree(object):
    __slots__ = '_root'

    def __init__(self):
        self._root = None

    @property
    def root(self):
        return self._root

    @root.setter
    def root(self, value):
        self._root = value

    def is_empty(self):
        return self._root is None

    def depth(self, x):
        if x.is_root():
            return 0
        else:
            return 1 + self.depth(x.parent)

    def _height(self, x):
        if x.is_leaf():
            return 0
        else:
            return 1 + max(self._height(c) for c in x.children)

    def height(self):
        return self._height(self._root)

    def preorder(self, x, func):
        if not self.is_empty():
            func(x.data)
            for c in x.children:
                self.preorder(c, func)

    def postorder(self, x, func):
        if not self.is_empty():
            for c in x.children:
                self.postorder(c, func)
            func(x.data)

    def __str__(self):
        return str(self._root)

    def find_parent_root_child(self, node):
        root = self.root
        if node == root:
            raise Exception("Root has no parent")
        current_node = node
        while current_node.parent != root:
            current_node = current_node.parent
        return current_node





    # def breadth_first(self):
    #     """
    #     Metoda vrši obilazak stabla po širini.
    #     """
    #     to_visit = Queue()
    #     to_visit.enqueue(self.root)
    #     while not to_visit.is_empty():
    #         e = to_visit.dequeue()
    #         print(e.data)
    #
    #         for c in e.children:
    #             to_visit.enqueue(c)


if __name__ == '__main__':
    pass
    # # instanca stabla
    # t = Tree()
    # t.root = TreeNode(0)
    #
    # # kreiranje relacija između novih čvorova
    # a = TreeNode(1)
    # b = TreeNode(2)
    # c = TreeNode(3)
    #
    # t.root.add_child(a)
    # t.root.add_child(c)
    # a.add_child(b)
    #
    # # visina stabla
    # print('Visina = %d' % t.height())
    #
    # # dubina čvora
    # print('Dubina(a) = %d' % t.depth(a))
    #
    # # obilazak po dubini - preorder
    # print('PREORDER')
    # t.preorder(t.root)
    #
    # # obilazak po dubini - postorder
    # print('POSTORDER')
    # t.postorder(t.root)
    #
    # # obilazak po širini
    # print('BREADTH FIRST')
    # # t.breadth_first()
    # print(t)
