import heapq
from Node import HuffNode



class HuffmanCoding(object):


    def __init__(self) -> None:
        self._root = None
        self.heap = []
        self.codes = {}
        self.reverseMapping = {}


    def getRoot(self) -> HuffNode:
        """ Returns the root node of the Huffman Tree
        
        Returns
        -----
            HuffNode -- [description]
        """
        return self._root


    def _setRoot(self, newRoot: HuffNode) -> None:
        """ Set a new root for the Huffman Tree
        
        Parameters
        -----
            newRoot (HuffNode) -- new root of the tree
        """
        if not isinstance(newRoot, HuffNode):
            raise TypeError('not and instance of HuffNode')
        self._root = newRoot


    def isLeaf(self) -> bool:
        """ Tell if the current node instance is a leaf.
        
        Returns
        -----
            bool -- True if the current instance is a leaf
        """
        return not self.left and not self.right


    def scanTree(self, root: HuffNode) -> None:
        """Scan the given Huffman tree in depth and print each encountered node.
        
        Parameters
        -----
            root (HuffNode) -- given root node of the Huffman tree
        """
        if root:
            print(root)

        if root.left:
            self.scanTree(root.left)

        if root.right:
            self.scanTree(root.right)


    ##TODO: see if it's possible to use an iterator over the text
    def makeFreqMap(self, text: str) -> dict:
        """ Build the frequency map of each character
        in the given text.
        
        Parameters
        -----
            text (str) -- source text
        
        Returns
        -----
            dict -- dictionnary of word frequencies
        """
        freqMap = {}
        for char in text:
            if char not in freqMap.keys():
                freqMap[char] = 1
            else:
                freqMap[char] += 1

        return freqMap


    def makeHeap(self, freqMap: dict) -> None:
        """Build a heap of Huffman nodes based on
        the given frequencies map.
        
        Parameters
        -----
            freqMap (dict) -- source frequencies map

        Returns
        -----
            list -- resulting heap as a list.
        """
        heap = []
        n = None

        for k,v in freqMap.items():
            n = HuffNode(k, v)
            heapq.heappush(heap, n)
        
        return heap


    def mergeNodes(self, heap) -> None:
        """ Merge each nodes from a given heap until only one is left.
        Each iteration adds the two lowest nodes by their frequencies, and merges them into a new one.
        """
        n1, n2 = None, None
        father = None

        while(len(heap) > 1):
            n1 = heapq.heappop(heap)        # get the two nodes with the lowest
            n2 = heapq.heappop(heap)        # frequencies of the heap
            father = n1 + n2                # merging nodes by using the overrided add operator
            heapq.heappush(heap, father)    # adding the new father node

        self._setRoot(heap[0])   # set the final resulting node as root of the Huffman Tree
