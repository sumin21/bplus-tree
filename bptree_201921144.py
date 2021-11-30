import sys
import math


def checkkey(arr, k):
    if k in arr:
        return True
    return False


def plusList(arr1, arr2):
    result = arr1
    for i in arr2:
        result.append(i)
    return result


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

    # print tree
    def print_childs(self):
        if(len(self.subTrees) > 0):
            print(self.keys, end='-')

            for n in self.subTrees:
                if(n != self.subTrees[len(self.subTrees) - 1]):
                    print(n.keys, end=',')
                else:
                    print(n.keys, end='\n')
            for n in self.subTrees:
                n.print_childs()

    # keys in leaf nodes
    def printLeafs(self, li):
        if(len(self.subTrees) > 0):
            for n in self.subTrees:
                n.printLeafs(li)
        else:
            for key in self.keys:
                li.append(key)

    # leaf nodes
    def findFakeLeftNode(self, li):
        if(len(self.subTrees) > 0):
            for n in self.subTrees:
                n.findFakeLeftNode(li)
        else:
            li.append(self)

    # first key of tree
    def keyValueFind(self):
        if(self.isLeaf):
            return self.keys[0]
        else:
            result = self.subTrees[0].keyValueFind()
            return result


class B_PLUS_TREE:

    def __init__(self, order):
        # order is degree of tree
        self.order = order
        self.root = Node()
        self.root.isLeaf = True
        self.root.isRoot = True

    def insert(self, k):

        self.root.keys.append(k)
        self.root.keys.sort()

        # root == leaf
        if(self.root.isRoot and self.root.isLeaf):

            # len exceed
            if(len(self.root.keys) == self.order):
                # split index
                rootSplitIndex = math.floor(self.order/2)
                rootSplitElement = self.root.keys[rootSplitIndex]

                leftArr = self.root.keys[0:rootSplitIndex]
                rightArr = self.root.keys[rootSplitIndex:]

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

                    # check
                    parentNode.subTrees[index].nextNode = childNode
                    # check
                    # indexx+2 없으면? (위에도)
                    if(len(parentNode.subTrees) > index + 2):
                        childNode.nextNode = parentNode.subTrees[index+2]

                    # 완성 --- parentNode = leaf+1 -------- childNode = leaf

                    # test (n이 결관데, n은 leaf 가 아니고 지금 key개수가 오버된 상황)

                    notLeafNode = parentNode  # 345

                    # overhead
                    while (len(notLeafNode.keys) >= self.order):
                        centerindex = math.floor(len(notLeafNode.keys)/2)  # 1
                        centernum = notLeafNode.keys[centerindex]  # 6

                        # parent 있다면
                        if(notLeafNode.parent):
                            p = notLeafNode.parent
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
                        for leftSubs in leftSubArr:
                            leftSubs.parent = newLeftNode

                        # new Leaf Right Node
                        notLeafNode.keys = rightArr
                        notLeafNode.parent = p
                        notLeafNode.isLeaf = False
                        notLeafNode.subTrees = rightSubArr

                        for rightSubs in rightSubArr:
                            rightSubs.parent = notLeafNode

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
        # 우선 k가 tree에 있는지 확인 !!
        node = self.findNode(k)[0]
        if(node == 0):
            print('None')
            return

        # 노드 최소 개수 (exceed ~ ) 5->2 아니냐?
        exceed = math.ceil(self.order/2) - 1

        # root == leaf
        if(self.root.isRoot and self.root.isLeaf):
            self.root.keys.remove(k)

        # root != leaf
        else:
            # node = leaf
            node.keys.remove(k)

            if node.isLeaf and len(node.keys) < exceed:
                p = node.parent
                nodeIndex = p.subTrees.index(node)

                leftSib = None
                rightSib = None
                fakeLeftNode = None
                fakeRightNode = None

                # node가 첫번째 자식 -> 무조건 right랑만
                if(nodeIndex == 0):
                    leftSib = None
                    rightSib = p.subTrees[1]
                    firstLeafNode = self.root

                    while not firstLeafNode.isLeaf:
                        firstLeafNode = firstLeafNode.subTrees[0]

                    # fakeLeft가 있는 경우
                    if node != firstLeafNode:
                        leafs = []
                        self.root.findFakeLeftNode(leafs)
                        for leaf in leafs:
                            if(leaf.nextNode == node):
                                fakeLeftNode = leaf
                                break

                # node가 마지막 자식 -> 무조건 left랑만
                elif(nodeIndex == len(p.subTrees)-1):
                    rightSib = None
                    leftSib = p.subTrees[len(p.subTrees) - 1]
                    fakeRightNode = node.nextNode

                # node가 가운데 자식 -> left, right 가능
                else:
                    leftSib = p.subTrees[nodeIndex - 1]
                    rightSib = node.nextNode  # None 일수도

                # left에서 못빌림------------
                if(leftSib == None or (leftSib != None and len(leftSib.keys) <= exceed)):
                    # right에서 못빌림 -> merge
                    if(rightSib == None or (rightSib != None and len(rightSib.keys) <= exceed)):
                        # right랑 merge (left 없)
                        if(leftSib == None):
                            newRightKeys = plusList(
                                node.keys, rightSib.keys)  # 8 10 11
                            rightSib.keys = newRightKeys
                            p.subTrees.remove(node)
                            del p.keys[0]  # 12

                            if(fakeLeftNode):
                                fakeLeftNode.nextNode = rightSib
                        # left랑 merge (right 없)
                        elif(rightSib == None):

                            newLeftKeys = plusList(leftSib.keys, node.keys)
                            leftSib.keys = newLeftKeys
                            p.subTrees.remove(node)
                            pKeyLen = len(p.keys)
                            del p.keys[pKeyLen-1]

                            leftSib.nextNode = None
                            if(fakeRightNode):
                                leftSib.nextNode = fakeRightNode
                        # left랑 merge (가운데 node)
                        else:
                            newLeftKeys = plusList(leftSib.keys, node.keys)
                            leftSib.keys = newLeftKeys
                            p.subTrees.remove(node)
                            del p.keys[nodeIndex-1]

                            leftSib.nextNode = rightSib

                    # right에서 빌리기
                    else:

                        right = rightSib.keys[0]
                        rightSib.keys.remove(right)

                        node.keys.append(right)
                        p.keys[nodeIndex] = rightSib.keys[0]

                # left에서 빌리기
                else:

                    left = leftSib.keys[len(leftSib.keys) - 1]
                    leftSib.keys.remove(left)

                    node.keys.insert(0, left)
                    p.keys[nodeIndex-1] = left

                node = p

            # remove k in key
            self.deleteNode(k)

            while(not node.isLeaf and len(node.keys) < exceed and not node.isRoot):
                p = node.parent
                nodeIndex = p.subTrees.index(node)  # 1

                leftSib = None
                rightSib = None

                # node가 첫번째 자식 -> 무조건 right랑만
                if(nodeIndex == 0):
                    rightSib = p.subTrees[1]
                    leftSib = None

                # node가 마지막 자식 -> 무조건 left랑만
                elif(nodeIndex == len(p.subTrees)-1):
                    leftSib = p.subTrees[len(p.subTrees) - 2]
                    rightSib = None

                # node가 가운데 자식 -> left, right 가능
                else:
                    leftSib = p.subTrees[nodeIndex - 1]
                    rightSib = node.nextNode  # None 일수도

                # left에서 못빌림------------
                if leftSib == None or (leftSib != None and len(leftSib.keys) <= exceed):
                    # right에서 못빌림 -> merge
                    if rightSib == None or (rightSib != None and len(rightSib.keys) <= exceed):
                        # right랑 merge (left 없)
                        if(leftSib == None):
                            pKey = p.keys[nodeIndex]

                            node.keys.append(pKey)
                            newRightKeys = plusList(node.keys, rightSib.keys)
                            p.subTrees.remove(node)
                            rightSib.keys = newRightKeys

                            for nodeSub in node.subTrees:
                                nodeSub.parent = rightSib

                            newRightSubs = plusList(
                                node.subTrees, rightSib.subTrees)
                            rightSib.subTrees = newRightSubs
                            p.keys.remove(pKey)

                        # left랑 merge (right 없)
                        else:
                            pKey = p.keys[nodeIndex - 1]
                            node.keys.insert(0, pKey)

                            newLeftKeys = plusList(leftSib.keys, node.keys)
                            p.subTrees.remove(node)
                            leftSib.keys = newLeftKeys
                            for nodeSub in node.subTrees:
                                nodeSub.parent = leftSib
                            newLeftSubs = plusList(
                                leftSib.subTrees, node.subTrees)
                            leftSib.subTrees = newLeftSubs

                            p.keys.remove(pKey)  # root []

                    # right에서 빌리기
                    else:
                        right = rightSib.keys[0]
                        rightSib.keys.remove(right)
                        rightSub = rightSib.subTrees[0]
                        rightSib.subTrees.remove(rightSub)

                        pKey = p.keys[nodeIndex]
                        node.subTrees.append(rightSub)

                        node.keys.append(pKey)
                        p.keys[nodeIndex] = right

                # left에서 빌리기
                else:

                    left = leftSib.keys[len(leftSib.keys) - 1]
                    leftSib.keys.remove(left)
                    leftSub = leftSib.subTrees[len(leftSib.subTrees) - 1]
                    leftSib.subTrees.remove(leftSub)

                    pKey = p.keys[nodeIndex-1]
                    node.subTrees.insert(0, leftSub)

                    node.keys.insert(0, pKey)
                    p.keys[nodeIndex-1] = left

                node = p
            # root = []

            # root
            if (node.isRoot):
                if(len(node.keys) == 0):
                    newRoot = node.subTrees[0]
                    del node  # node 삭제
                    newRoot.isRoot = True
                    newRoot.parent = None
                    self.root = newRoot

    def print_root(self):
        l = "["
        for k in self.root.keys:
            l += "{},".format(k)
        l = l[:-1] + "]"
        print(l)

    def print_tree(self):
        node = self.root
        if self.root.isLeaf:
            self.print_root()
        else:
            node.print_childs()

    def find_range(self, k_from, k_to):
        fromExist = self.findNode(k_from)
        toExist = self.findNode(k_to)
        if(fromExist and toExist):
            li = []
            self.root.printLeafs(li)
            fromIndex = li.index(k_from)
            toIndex = li.index(k_to)
            for i in range(fromIndex, toIndex + 1):
                if(i == toIndex):
                    print(li[i], end='\n')
                else:
                    print(li[i], end=',')

        else:
            print("존재하지 않음")

    def find(self, k):
        process = self.findNode(k)
        if(process[0] == 0):
            print('None')
        else:
            for i in process[1]:
                if(i == process[1][len(process[1]) - 1]):
                    print(i.keys, end='\n')
                else:
                    print(i.keys, end='-')

    def findNode(self, k):
        node = self.root
        processList = []
        while not node.isLeaf:
            processList.append(node)
            # k가 node에 있다면
            if(checkkey(node.keys, k)):
                index = node.keys.index(k) + 1  # index+1의 subtree
            else:
                if k < node.keys[0]:
                    index = 0
                else:
                    node.keys.append(k)
                    node.keys.sort()
                    index = node.keys.index(k)
                    node.keys.remove(k)

            node = node.subTrees[index]

        if node.isLeaf:
            if checkkey(node.keys, k):
                processList.append(node)
                return [node, processList]
            else:
                return 0

    def deleteNode(self, k):
        node = self.root
        while not node.isLeaf:
            index = 0
            # k가 node에 있다면
            if(checkkey(node.keys, k)):
                keyIndex = node.keys.index(k)
                kChildNode = node.subTrees[keyIndex+1]

                a = kChildNode.keyValueFind()
                node.keys[keyIndex] = a
                return
            elif len(node.keys) != 0:
                if k < node.keys[0]:
                    index = 0
                else:
                    node.keys.append(k)
                    node.keys.sort()
                    index = node.keys.index(k)
                    node.keys.remove(k)
            else:
                if(node.subTrees[0].isLeaf):
                    break
            node = node.subTrees[index]
        return


def main():
    myTree = None

    while (True):
        comm = sys.stdin.readline()
        comm = comm.replace("\n", "")
        params = comm.split()
        if len(params) < 1:
            continue

        # print(comm)

        if params[0] == "INIT":
            order = int(params[1])
            myTree = B_PLUS_TREE(order)

        elif params[0] == "EXIT":
            return

        elif params[0] == "INSERT":
            k = int(params[1])
            myTree.insert(k)

        elif params[0] == "DELETE":
            k = int(params[1])
            myTree.delete(k)

        elif params[0] == "ROOT":
            myTree.print_root()

        elif params[0] == "PRINT":
            myTree.print_tree()

        elif params[0] == "FIND":
            k = int(params[1])
            myTree.find(k)

        elif params[0] == "RANGE":
            k_from = int(params[1])
            k_to = int(params[2])
            myTree.find_range(k_from, k_to)

        elif params[0] == "SEP":
            print("-------------------------")


if __name__ == "__main__":
    main()
