class Node:
    def __init__(self):
        # each node can have |order - 1| keys
        self.keys = []

        # |order| / 2 <= # of subTree pointers <= |order|
        # [node1, node2]
        self.subTrees = []

        # pointer of parent
        self.parent = None

        #leafnode is true / false
        self.isLeaf = False

        # rootnode is true / false
        self.isRoot = False

        # if(leafnode)
        # leaf node has next node pointer
        self.nextNode = None
        self.values = []


def main():
    a = Node()
    a.keys = [1, 2]
    b = a
    b.keys = [3, 4]
    print(a.keys)


if __name__ == "__main__":
    main()
