#!/usr/bin/python
import time


class Tree ():
    def __init__(self, Nid, Pid, Left, Right, Expr):
        self.Nid       = Nid
        self.Pid       = Pid
        self.Left      = Left
        self.Right     = Right
        self.LeftChild = None
        self.RightChild= None
        self.Expr      = Expr
        self.Depth     = 0

    def IsLeaf (self):
        return (self.LeftChild == None and self.RightChild == None)
        

class DecisionTree ():
    
    def __init__(self, ElementNum):
        self.ElementNum = ElementNum
        self.TreeNode   = {}
        self.TreeLeaf   = []

    def NewNode (self,   Pid, Left, Right, Expr):
        Nid   = len (self.TreeNode)
        TNode = Tree (Nid, Pid, Left, Right, Expr)
        self.TreeNode [Nid] = TNode
        return TNode

    def GetExpr (self, Expr, Element, D=0):
        SrcList = list(self.Expr)
        Pos     = self.Expr.find (Expr) + D
        SrcList.insert(Pos, Element)
        return''.join(SrcList)

    def CreateTree (self, Pid, Element, Factor, Expr, D):
        #print ("---->[%d] CreateTree.Expr: %s, Element:%s <----" %(Pid, Expr, Element))
        if not Expr:
            Node = self.NewNode (Pid, Factor, Element, self.GetExpr (Factor, Element, D))
            self.TreeLeaf.append (Node)
            Node.Depth = self.TreeNode[Pid].Depth + 1
            return Node
        
        CmpIndex = int(len(Expr)/2)
        Node = self.NewNode (Pid, Expr[CmpIndex], Element, Expr[CmpIndex] + Element)
        Node.Depth = self.TreeNode[Pid].Depth + 1
     
        Node.LeftChild  = self.CreateTree (Node.Nid, Element, Node.Left, Expr[CmpIndex+1:len(Expr)], 1)
        Node.RightChild = self.CreateTree (Node.Nid, Element, Node.Left, Expr[0:CmpIndex], 0)

        return Node
        
    def GrowingTree (self, Element):
        print ("===> GrowingTree, Element = %s" %Element)
        LeafNum = len (self.TreeLeaf)

        # iterate all leaf nodes
        for Index in range (LeafNum):
            Leaf = self.TreeLeaf[0]
            self.TreeLeaf.pop (0)
            Index += 1

            self.Expr = Leaf.Expr

            # modify current leaf to a sub-tree root, split
            CmpIndex   = int(len(self.Expr)/2)
            
            Leaf.Left  = self.Expr[CmpIndex]
            Leaf.Right = Element
            Leaf.Expr  = Leaf.Left + Leaf.Right

            Leaf.LeftChild  = self.CreateTree (Leaf.Nid, Element, Leaf.Left, self.Expr[CmpIndex+1:len(self.Expr)], 1)
            Leaf.RightChild = self.CreateTree (Leaf.Nid, Element, Leaf.Left, self.Expr[0:CmpIndex], 0)

        print ("Element[%s]LeafNode count: %d" %(Element, len (self.TreeLeaf)))
        return

    def DumpTree (self, Tag=""):
        print ("\r\nStart dumping tree...")
        Name = "DecisionTree_" + str(self.ElementNum) + "-elements"
        File = open(Name + ".dot" , "w")

        #header
        File.write("digraph \"" + Name + "\"{\n")
        File.write("\tlabel=\"" + Name + "\";\n")

        LeafNode = 0

        Queue  = []
        QIndex = 0
        Queue.append (self.TreeNode[0])
        while QIndex < len(Queue):
            # pop the first node of queue
            TNode = Queue[QIndex]
            QIndex += 1

            #write node
            Label = ""
            for ch in TNode.Expr:
                Label += "a" + str(ch) + "<"
            Label = Label[:-1]  

            if TNode.IsLeaf ():
                LeafNode += 1
                File.write("\tN" + str(TNode.Nid) + "[color=red, label=\"{" + Label + "}\"]\n")
                continue
            else:
                File.write("\tN" + str(TNode.Nid) + "[color=black, label=\"{" + Label + "}\"]\n")

            #write edges
            LTree = TNode.LeftChild
            Queue.append (LTree)
            File.write("\tN" + str(TNode.Nid) + " -> N" + str(LTree.Nid) + "[color=blue" + ",label=\"{T}\"]\n")

            RTree = TNode.RightChild
            Queue.append (RTree)
            File.write("\tN" + str(TNode.Nid) + " -> N" + str(RTree.Nid) + "[color=blue" + ",label=\"{F}\"]\n")
        File.write("}\n")
        File.close()

        print ("Total leaves: %d" %(LeafNode))
  
    def BuildTree (self):
        # create elements
        ElementSet = []
        for No in range (self.ElementNum):
            ElementSet.append (str(No+1))
        print (ElementSet)

        # Initiate root node
        Element = ElementSet[0]
        Root = self.NewNode (-1, Element, Element, Element)
        self.TreeLeaf.append (Root)
        ElementSet.remove (Element)

        Root.Depth = 0;
        
        # insert other node into the tree
        for Element in ElementSet:
            self.GrowingTree (Element)
        
        self.DumpTree ();




