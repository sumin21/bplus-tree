# root == leaf

if(self.root.isRoot and self.root.isLeaf):
    self.root.values.append(k)

    # len exceed
    if(len(self.root.keys) == self.order):
        # split index
        rootSplitIndex = math.floor(self.order/2)
        rootSplitElement = self.root.keys[rootSplitIndex]

        leftArr = self.root.keys[0:rootSplitIndex]
        rightArr = self.root.keys[rootSplitIndex:]

        self.root.keys = [rootSplitElement]
        self.root.isLeaf = False
        self.root.values = []

        # new Leaf Left Node
        newLeafLeftNode = Node()
        newLeafLeftNode.isLeaf = True
        newLeafLeftNode.parent = self.root
        newLeafLeftNode.keys = leftArr
        newLeafLeftNode.values = leftArr

        # new Leaf Right Node
        newLeafRightNode = Node()
        newLeafRightNode.isLeaf = True
        newLeafRightNode.parent = self.root
        newLeafRightNode.keys = rightArr
        newLeafRightNode.values = rightArr

        newLeafLeftNode.nextNode = newLeafRightNode

        self.root.subTrees = [newLeafLeftNode, newLeafRightNode]
