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
        self.keys = []
        self.subTrees = []
        self.parent = None
        self.isLeaf = False
        self.isRoot = False
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

    # leaf nodes
    def leafNodes(self, li):
        if(len(self.subTrees) > 0):
            for n in self.subTrees:
                n.leafNodes(li)
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
        index = 0

        if(self.root.isRoot and self.root.isLeaf):
            childNode = self.root

        else:
            childNode = self.root
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
            childNode.values.append(k)

            # leaf len exceed
            if(len(childNode.keys) == self.order):
                splitIndex = math.floor(self.order/2)  # 1
                parentNode = None

                if(childNode.isRoot):
                    parentNode = Node()
                    parentNode.isRoot = True
                    childNode.isRoot = False
                    self.root = parentNode
                    childNode.parent = parentNode
                    parentNode.subTrees.append(childNode)

                else:
                    parentNode = childNode.parent  # root+1

                # center into parentNode
                parentNode.keys.append(
                    childNode.keys[splitIndex])  # root = 345
                parentNode.keys.sort()  # 이렇게 안하고 index 에 바로 넣어도 됨

                # new Leaf Left Node
                newLeafLeftNode = Node()
                newLeafLeftNode.isLeaf = True
                newLeafLeftNode.parent = parentNode
                newLeafLeftNode.keys = childNode.keys[0:splitIndex]
                newLeafLeftNode.values = childNode.values[0:splitIndex]

                # new Leaf Right Node
                childNode.keys = childNode.keys[splitIndex:]
                childNode.values = childNode.values[splitIndex:]

                parentNode.subTrees.insert(index, newLeafLeftNode)

                fakeLeftNode = self.findFakeLeft(newLeafLeftNode, childNode)

                if(fakeLeftNode != None):
                    fakeLeftNode.nextNode = newLeafLeftNode

                # check
                newLeafLeftNode.nextNode = childNode

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
                        notLeafNode.parent = p
                        p.subTrees.append(notLeafNode)

                    leftArr = notLeafNode.keys[0:centerindex]  # 3
                    rightArr = notLeafNode.keys[centerindex+1:]  # 5
                    leftSubArr = notLeafNode.subTrees[0:centerindex+1]
                    rightSubArr = notLeafNode.subTrees[centerindex+1:]

                    notLeafNode.keys.remove(centernum)  # 35

                    # new Leaf Left Node
                    newLeftNode = Node()
                    newLeftNode.parent = p
                    newLeftNode.keys = leftArr

                    newLeftNode.subTrees = leftSubArr
                    for leftSubs in leftSubArr:
                        leftSubs.parent = newLeftNode

                    # new Leaf Right Node
                    notLeafNode.keys = rightArr
                    notLeafNode.subTrees = rightSubArr

                    p.keys.append(centernum)  # 4
                    p.keys.sort()
                    indexx = p.keys.index(centernum)  # 0
                    p.subTrees.insert(indexx, newLeftNode)

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
                    fakeLeftNode = self.findFakeLeft(node, node)

                # node가 마지막 자식 -> 무조건 left랑만
                elif(nodeIndex == len(p.subTrees)-1):
                    rightSib = None
                    index = len(p.subTrees) - 2
                    leftSib = p.subTrees[index]
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
                        # left랑 merge
                        else:
                            newLeftKeys = plusList(leftSib.keys, node.keys)
                            leftSib.keys = newLeftKeys
                            p.subTrees.remove(node)

                            del p.keys[nodeIndex-1]

                            if(rightSib):
                                leftSib.nextNode = rightSib
                            else:
                                leftSib.nextNode = None
                                if(fakeRightNode):
                                    leftSib.nextNode = fakeRightNode

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
                        rightSub.parent = node

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
                    leftSub.parent = node

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
        if(len(self.root.keys) == 0):
            print('[]')
        else:
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
        fromExist = self.findNode(k_from)[0]
        toExist = self.findNode(k_to)[0]
        if(fromExist and toExist):
            li = []
            while fromExist != toExist:
                for key in fromExist.keys:
                    li.append(key)

                fromExist = fromExist.nextNode

            if fromExist == toExist:
                for key in toExist.keys:
                    li.append(key)

            fromIndex = li.index(k_from)
            toIndex = li.index(k_to)
            for i in range(fromIndex, toIndex):
                print(li[i], end=',')
            print(li[toIndex], end='\n')

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

    def findFakeLeft(self, node, child):
        fakeLeftNode = None
        firstLeafNode = self.root

        while not firstLeafNode.isLeaf:
            firstLeafNode = firstLeafNode.subTrees[0]

        # fakeLeft가 있는 경우
        if node != firstLeafNode:
            leafs = []
            self.root.leafNodes(leafs)

            for leaf in leafs:
                if(leaf.nextNode == child):
                    fakeLeftNode = leaf
                    break
        return fakeLeftNode


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
