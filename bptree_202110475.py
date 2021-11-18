import sys
import math


class Node:
    def __init__(self):
        # each node can have |order - 1| keys
        self.keys = []

        # |order| / 2 <= # of subTree pointers <= |order|
        # [node1, node2]
        self.subTrees = []

        # pointer of parent
        self.parent = None

        # leafnode is true / false
        self.isLeaf = False

        # rootnode is true / false
        self.isRoot = False

        # if(leafnode)
        # leaf node has next node pointer
        self.nextNode = None
        self.values = []

    def print_childs(self):
        if(len(self.subTrees) > 0):
            for n in self.subTrees:
                print(n.keys)
                n.print_childs()


class B_PLUS_TREE:

    def __init__(self, order):
        # order is degree of tree
        self.order = order
        self.root = Node()
        self.root.isLeaf = True
        self.root.isRoot = True

    def insert(self, k):

        # root == leaf
        if(self.root.isRoot and self.root.isLeaf):
            self.root.keys.append(k)

            # sorting
            self.root.keys.sort()

            # len exceed
            if(len(self.root.keys) == self.order):
                # split index
                rootSplitIndex = math.floor(self.order/2)
                rootSplitElement = self.root.keys[rootSplitIndex]
                print(type(rootSplitElement))
                print(rootSplitElement)
                leftArr = self.root.keys[0:rootSplitIndex]
                rightArr = self.root.keys[rootSplitIndex:]

                print(leftArr)
                print(rightArr)

                self.root.keys = [rootSplitElement]
                self.root.isLeaf = False

                # new Leaf Left Node
                newLeafLeftNode = Node()
                newLeafLeftNode.isLeaf = True
                newLeafLeftNode.parent = self.root
                newLeafLeftNode.keys = leftArr

                # new Leaf Right Node
                newLeafRightNode = Node()
                newLeafRightNode.isLeaf = True
                newLeafRightNode.parent = self.root
                newLeafRightNode.keys = rightArr

                newLeafLeftNode.nextNode = newLeafRightNode

                self.root.subTrees = [newLeafLeftNode, newLeafRightNode]

        # else
        else:
            # 반복
            self.root.keys.append(k)
            self.root.keys.sort()
            index = self.root.keys.index(k)  # 2
            childNode = self.root.subTrees[index]
            self.root.keys.remove(k)

            # ------------
            while not childNode.isLeaf:
                childNode.keys.append(k)
                childNode.keys.sort()
                index = childNode.keys.index(k)
                childNode.keys.remove(k)
                childNode = childNode.subTrees[index]

            # (end) if(leaf node)
            if(childNode.isLeaf):
                childNode.keys.append(k)
                childNode.keys.sort()  # 568

                # leaf len exceed
                if(len(childNode.keys) == self.order):
                    splitIndex = math.floor(len(childNode.keys)/2)  # 1
                    parentNode = childNode.parent  # root+1

                    # center into parentNode
                    parentNode.keys.append(
                        childNode.keys[splitIndex])  # root = 345
                    parentNode.keys.sort()  # 이렇게 안하고 index 에 바로 넣어도 됨

                    leftArr = childNode.keys[0:splitIndex]  # 4
                    rightArr = childNode.keys[splitIndex:]  # 56

                    # new Leaf Left Node
                    newLeafLeftNode = Node()
                    newLeafLeftNode.isLeaf = True
                    newLeafLeftNode.parent = parentNode
                    newLeafLeftNode.keys = leftArr

                    # new Leaf Right Node
                    childNode.keys = rightArr
                    childNode.parent = parentNode

                    parentNode.subTrees.insert(index, newLeafLeftNode)
                    if(index != 0):
                        parentNode.subTrees[index -
                                            1].nextNode = newLeafLeftNode

                    print("check newLeafLeftNode")
                    print(parentNode.subTrees[index] == newLeafLeftNode)

                    # check
                    parentNode.subTrees[index].nextNode = childNode
                    # check
                    # indexx+2 없으면? (위에도)
                    if(len(parentNode.subTrees) > index + 2):
                        childNode.nextNode = parentNode.subTrees[index+2]

                    # 완성 --- parentNode = leaf+1 -------- childNode = leaf

                    # test (n이 결관데, n은 leaf 가 아니고 지금 key개수가 오버된 상황)

                    notLeafNode = parentNode  # 345
                    print('notleaf key개수:' + str(len(notLeafNode.keys)))
                    print(notLeafNode.keys)
                    kk = 1
                    # overhead
                    while (len(notLeafNode.keys) >= self.order) and (kk < 10):
                        kk += 1
                        centerindex = math.floor(len(notLeafNode.keys)/2)  # 1
                        centernum = notLeafNode.keys[centerindex]  # 6

                        # parent 있다면
                        if(notLeafNode.parent):
                            p = notLeafNode.parent
                            print('parent 있어')
                        else:
                            p = Node()
                            p.isRoot = True
                            self.root = p
                            notLeafNode.isRoot = False
                            p.subTrees.append(notLeafNode)

                        leftArr = notLeafNode.keys[0:centerindex]  # 3
                        rightArr = notLeafNode.keys[centerindex+1:]  # 5

                        # 12, 3
                        leftSubArr = notLeafNode.subTrees[0:centerindex+1]
                        # 4, 56
                        rightSubArr = notLeafNode.subTrees[centerindex+1:]

                        notLeafNode.keys.remove(centernum)  # 35

                        # new Leaf Left Node
                        newLeftNode = Node()
                        newLeftNode.isLeaf = False
                        newLeftNode.parent = p
                        newLeftNode.keys = leftArr

                        newLeftNode.subTrees = leftSubArr

                        # new Leaf Right Node
                        notLeafNode.keys = rightArr
                        notLeafNode.parent = p
                        notLeafNode.isLeaf = False
                        notLeafNode.subTrees = rightSubArr

                        p.keys.append(centernum)  # 4
                        p.keys.sort()
                        indexx = p.keys.index(centernum)  # 0
                        p.subTrees.insert(indexx, newLeftNode)

                        if(indexx != 0):
                            p.subTrees[indexx - 1].nextNode = newLeftNode
                        newLeftNode.nextNode = notLeafNode

                        # indexx+2 없으면? (위에도)
                        if(len(p.subTrees) > indexx + 2):
                            notLeafNode.nextNode = p.subTrees[indexx + 2]

                        notLeafNode = p

    def delete(self, k):
        pass

    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)
        pass

    def print_tree(self):
        print('루트 : ')
        print(self.root.keys)

        node = self.root
        node.print_childs()

    def find_range(self, k_from, k_to):
        pass

    def find(self, k):
        pass


def main():
    myTree = None

    while (True):
        comm = sys.stdin.readline()
        comm = comm.replace("\n", "")
        params = comm.split()
        if len(params) < 1:
            continue

        print(comm)

        if params[0] == "INIT":
            order = int(params[1])
            myTree = B_PLUS_TREE(order)

        elif params[0] == "EXIT":
            return

        elif params[0] == "INSERT":
            k = int(params[1])
            myTree.insert(k)

        # elif params[0] == "DELETE":
        #     k = int(params[1])
        #     myTree.delete(k)

        # elif params[0] == "ROOT":
        #     myTree.print_root()

        elif params[0] == "PRINT":
            myTree.print_tree()

        # elif params[0] == "FIND":
        #     k = int(params[1])
        #     myTree.find(k)

        # elif params[0] == "RANGE":
        #     k_from = int(params[1])
        #     k_to = int(params[2])
        #     myTree.find_range(k_from, k_to)

        elif params[0] == "SEP":
            print("-------------------------")


if __name__ == "__main__":
    main()
